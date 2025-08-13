from sqlalchemy import Column, Integer, String
from modelbase import ModelBase

class Kullanici(ModelBase):
    __tablename__ = "kullanicilar"
    id = Column(Integer, primary_key=True)
    ad = Column(String)
    soyad = Column(String)
    yas = Column(Integer)
    toplamkira = Column(Integer, default=0)
    aktifkira = Column(Integer, default=0)