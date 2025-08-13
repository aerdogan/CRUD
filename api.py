from fastapi import FastAPI
from controllers import Home, Kitap, Kullanici, Hareket

app = FastAPI(title="My API", version="1.0.0")

app.include_router(Home.router, prefix="", tags=["Root"])
app.include_router(Kitap.router, prefix="/kitap", tags=["Kitap"])
app.include_router(Kullanici.router, prefix="/kullanici", tags=["Kullanıcı"])
app.include_router(Hareket.router, prefix="/hareket", tags=["Hareket"])