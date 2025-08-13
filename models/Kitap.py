from sqlalchemy import Boolean, Column, Integer, String
from modelbase import ModelBase

class Kitap(ModelBase):
    __tablename__ = "kitaplar"
    id = Column(Integer, primary_key=True)
    ad = Column(String)
    yayinevi = Column(String)
    kirada = Column(Boolean, default=False)
    toplamkira = Column(Integer, default=0)


