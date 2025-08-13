from enum import Enum
from sqlalchemy import Column, Enum as SQLEnum, Integer, DateTime
from modelbase import ModelBase

class TeslimDurumuEnum(str, Enum):
    TESLIM_ETTI = "Teslim Etti"
    TESLIM_ALDI = "Teslim Aldı"
    
class Hareket(ModelBase):
    __tablename__ = "hareketler"
    id = Column(Integer, primary_key=True)
    tarih = Column(DateTime)
    kitap_id = Column(Integer)
    kullanici_id = Column(Integer)
    durum = Column(SQLEnum(TeslimDurumuEnum), default=TeslimDurumuEnum.TESLIM_ETTI)
