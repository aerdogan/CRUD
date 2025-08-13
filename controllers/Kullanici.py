from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Kullanici
from data import get_db

class KullaniciCreate(BaseModel):
    ad: str
    soyad: str
    yas: int    

class KullaniciResponse(BaseModel):
    id: int
    ad: str
    soyad: str
    yas: int
    toplamkira:int
    aktifkira:int

    class Config:
        from_attributes = True
    
#CRUD
router = APIRouter()

# Kullanıcı ekleme
@router.post("/kullaniciekle", response_model=KullaniciResponse)
def kullanici_ekle(kullanici: KullaniciCreate, db: Session = Depends(get_db)):
    yeni_kullanici = Kullanici(ad=kullanici.ad, soyad=kullanici.soyad, yas = kullanici.yas )    
    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)
    return yeni_kullanici

# Kullanıcı listeleme
@router.get("/kullanicilistele", response_model=List[KullaniciResponse])
def kullanici_listele(db: Session = Depends(get_db)):   
    return db.query(Kullanici).all()

# Kullanıcı filtreleme
@router.get("/kullanicifiltrele", response_model=List[KullaniciResponse])
def kullanici_filtrele(
    ad: Optional[str] = Query(None, description="Ad ile arama"),
    soyad: Optional[str] = Query(None, description="Soyad ile arama"),
    db: Session = Depends(get_db)
):
    query = db.query(Kullanici)

    if ad:
        query = query.filter(Kullanici.ad.ilike(f"%{ad}%"))
    if soyad:
        query = query.filter(Kullanici.soyad.ilike(f"%{soyad}%"))

    return query.all()

#güncelle
@router.put("/kullaniciguncelle/{id}", response_model=KullaniciResponse)
def kullanici_guncelle(
    id: int,
    kullanici_data: KullaniciResponse,  # Burada istersen ayrı bir schema da kullanabilirsin (UpdateKullanici)
    db: Session = Depends(get_db)
):
    kullanici = db.query(Kullanici).filter(Kullanici.id == id).first()
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    # Alanları güncelle
    kullanici.ad = kullanici_data.ad
    kullanici.soyad = kullanici_data.soyad
    db.commit()
    db.refresh(kullanici)
    return kullanici

#silme
@router.delete("/kullanicisil/{id}")
def kullanici_sil(id: int, db: Session = Depends(get_db)):
    kullanici = db.query(Kullanici).filter(Kullanici.id == id).first()
    if not kullanici:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    db.delete(kullanici)
    db.commit()
    return {"detail": "Kullanıcı başarıyla silindi"}