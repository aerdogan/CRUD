from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import Home, Kitap, Kullanici, Hareket

app = FastAPI(title="My API", version="1.0.0")

origins = [
    "http://localhost:4200",   # Angular local development
]

# Middleware ekleme
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # İzin verilen origin listesi
    allow_credentials=True,         # Cookie/Authorization header'ına izin
    allow_methods=["*"],             # Tüm HTTP metodlarına izin
    allow_headers=["*"],             # Tüm header’lara izin
)

app.include_router(Home.router, prefix="", tags=["Root"])
app.include_router(Kitap.router, prefix="/kitap", tags=["Kitap"])
app.include_router(Kullanici.router, prefix="/kullanici", tags=["Kullanıcı"])
app.include_router(Hareket.router, prefix="/hareket", tags=["Hareket"])