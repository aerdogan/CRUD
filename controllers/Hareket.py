from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from data import get_db
from models import Hareket, Kitap, Kullanici
from models.Hareket import TeslimDurumuEnum

class HareketResponse(BaseModel):
    id: int
    tarih: datetime
    kitap_id: int
    kullanici_id: int
    durum: TeslimDurumuEnum

    class Config:
        from_attributes = True
        
router = APIRouter()

# 1️⃣ Hareketleri listele
@router.get("/hareketlistele", response_model=List[HareketResponse])
def hareket_listele(db: Session = Depends(get_db)):
    return db.query(Hareket).all()


# 2️⃣ Hareket filtreleme (kullanıcı veya kitap bazlı)
@router.get("/hareketfiltrele", response_model=List[HareketResponse])
def hareket_filtrele(
    kullanici_id: Optional[int] = Query(None),
    kitap_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Hareket)
    if kullanici_id:
        query = query.filter(Hareket.kullanici_id == kullanici_id)
    if kitap_id:
        query = query.filter(Hareket.kitap_id == kitap_id)
    return query.all()

# 3️⃣ Kitap kirala (yeni hareket oluştur)
@router.post("/kirala", response_model=dict)
def kitap_kirala(
    kitap_id: int,
    kullanici_id: int,
    db: Session = Depends(get_db)
):
    # Kitap var mı kontrol
    kitap = db.query(Kitap).filter(Kitap.id == kitap_id).first()
    if not kitap:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    
    if kitap.kirada:
        raise HTTPException(status_code=404, detail="Kitap kiralanamaz")

    # Kullanıcı var mı kontrol
    kullanici = db.query(Kullanici).filter(Kullanici.id == kullanici_id).first()
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    # Hareket oluştur
    hareket = Hareket(
        tarih=datetime.now(),
        kitap_id=kitap_id,
        kullanici_id=kullanici_id,
        durum=TeslimDurumuEnum.TESLIM_ALDI  # kiralandı → teslim alındı
    )
    db.add(hareket)
    kitap.kirada = True  # kitap artık kirada
    kitap.toplamkira += 1

    kullanici.toplamkira += 1
    kullanici.aktifkira += 1

    db.commit()
    db.refresh(hareket)
    return {"detail": "Kitap başarıyla kiralandı", "hareket_id": hareket.id}

# 4️⃣ Kitap teslim et (mevcut hareketi güncelle)
@router.put("/teslimet/{hareket_id}", response_model=dict)
def kitap_teslim_et(
    hareket_id: int,
    db: Session = Depends(get_db)
):
    hareket = db.query(Hareket).filter(Hareket.id == hareket_id).first()
    if not hareket:
        raise HTTPException(status_code=404, detail="Hareket bulunamadı")
    hareket.durum = TeslimDurumuEnum.TESLIM_ETTI

    kitap = db.query(Kitap).filter(Kitap.id == hareket.kitap_id).first()
    kullanici = db.query(Kullanici).filter(Kullanici.id == hareket.kullanici_id).first()

    if kitap:
        kitap.kirada = False

    if kullanici:
        kullanici.aktifkira -= 1

    db.commit()
    return {"detail": "Kitap başarıyla teslim edildi"}

# 5️⃣ Hareket sil
@router.delete("/hareketsil/{hareket_id}")
def hareket_sil(hareket_id: int, db: Session = Depends(get_db)):
    hareket = db.query(Hareket).filter(Hareket.id == hareket_id).first()
    if not hareket:
        raise HTTPException(status_code=404, detail="Hareket bulunamadı")
    
    kitap = db.query(Kitap).filter(Kitap.id == hareket.kitap_id).first()
    kullanici = db.query(Kullanici).filter(Kullanici.id == hareket.kullanici_id).first()

    if kitap:
        kitap.kirada = False

    if kullanici:
        kullanici.aktifkira -= 1                

    db.delete(hareket)
    db.commit()
    return {"detail": "Hareket başarıyla silindi"}
