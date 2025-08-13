from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Hareket, Kitap
from data import get_db

class KitapCreate(BaseModel):
    ad: str
    yayinevi: str

class KitapResponse(BaseModel):
    id: int
    ad: str
    yayinevi: str
    kirada: bool
    toplamkira: int

    class Config:
        from_attributes = True
    
#CRUD
router = APIRouter()

# Kitap ekleme
@router.post("/kitapekle", response_model=KitapResponse)
def kitap_ekle(kitap: KitapCreate, db: Session = Depends(get_db)):
    yeni_kitap = Kitap(ad=kitap.ad, yayinevi=kitap.yayinevi, kirada=False)    
    db.add(yeni_kitap)
    db.commit()
    db.refresh(yeni_kitap)

# Kitap listeleme
@router.get("/kitaplistele", response_model=List[KitapResponse])
def kitap_listele(db: Session = Depends(get_db)):   
    return db.query(Kitap).all()


# Kitap filtreleme
@router.get("/kitapfiltrele", response_model=List[KitapResponse])
def kitap_filtrele(
    ad: Optional[str] = Query(None, description="Kitap adı ile arama"),
    yayinevi: Optional[str] = Query(None, description="Yayınevi ile arama"),
    kirada: Optional[bool] = Query(None, description="Kira bilgisine göre arama"),
    db: Session = Depends(get_db)
):
    query = db.query(Kitap)

    if ad:
        query = query.filter(Kitap.ad.ilike(f"%{ad}%"))
    if yayinevi:
        query = query.filter(Kitap.yayinevi.ilike(f"%{yayinevi}%"))
    if (kirada == True or kirada == False ):
        query = query.filter(Kitap.kirada == kirada)

    return query.all()

# Kitap güncelleme
@router.put("/kitapguncelle/{id}", response_model=KitapResponse)
def kitap_guncelle(
    id: int,
    kitap_data: KitapCreate,
    db: Session = Depends(get_db)
):
    kitap = db.query(Kitap).filter(Kitap.id == id).first()
    if not kitap:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")

    # Alanları güncelle
    kitap.ad = kitap_data.ad
    kitap.yayinevi = kitap_data.yayinevi
    kitap.kirada = kitap_data.kirada
    db.commit()
    db.refresh(kitap)
    return kitap

# Kitap silme
@router.delete("/kitapsil/{id}")
def kitap_sil(id: int, db: Session = Depends(get_db)):
    kitap = db.query(Kitap).filter(Kitap.id == id).first()
    if not kitap:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")

    db.delete(kitap)
    db.commit()
    return {"detail": "Kitap başarıyla silindi"}