from fastapi import FastAPI, Request, status, HTTPException
from model import *
from database import sessionLocal
import uvicorn
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa****************f7099f6f0f4caa6cf63b88e8d3e7"

# encryption algorithm
ALGORITHM = "HS256"

# Pydantic Model that will be used in the
# token endpoint for the response


class Token(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()
db = sessionLocal()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/")
def index():
    return ("ini indeks")


def create_access_token(data: dict):
    to_encode = data.copy()

    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # return the generated token
    return encoded_jwt

# the endpoint to get the token


@app.get("/get_token")
async def get_token():

    # data to be signed using token
    data = {
        'info': 'secret information',
        'from': 'GFG'
    }
    token = create_access_token(data=data)
    return {'token': token}


@app.post("/verify_token")
async def verify_token(token: str):
    try:
        # try to decode the token, it will
        # raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def authenticate_user(username: str, password: str):
    if username == "admin" and password == "password":
        return {"username": username}
    return None


@app.post("/Login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token["sub"]
    except jwt.JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")

    return {"message": f"Welcome, {username}!"}


@app.get("/kategori", tags=['Kategori'])
def kategori():
    query = db.query(Kategori).all()
    data = [x.nama for x in query]
    db.close()
    return {'kategori ': data}


@app.get("/kategori/{id}", tags=['Kategori'])
def kategori(id):
    data = db.query(Kategori).filter(Kategori.id == id).first()
    print(data)
    db.close()
    if data:
        return {"nama kategori": data.nama}
    else:
        return {"status ": "id tidak ditemukan"}


@app.get("/product", tags=['Product'])
def product():
    query = db.query(Product).all()
    data = [x.nama for x in query]
    db.close()
    return {'product ': data}


@app.get("/product/{id}", tags=['Product'])
def product(id):
    data = db.query(Product).filter(Product.id == id).first()
    print(data)
    db.close()
    if data:
        return {"nama product": data}
    else:
        return {"status ": "id tidak ditemukan"}


@app.post("/kategori/{}", tags=['Kategori'])
def tambah_kategori(namakategori: str):
    data = Kategori(nama=namakategori)
    db.add(data)
    db.commit()
    db.close()
    return {"status": "Ok", "kategori": namakategori}


@app.delete("/kategori/{id}", tags=['Kategori'])
def hapus_kategori(id: int):
    data = db.query(Kategori).filter(Kategori.id == id).first()
    print(data)
    if data:
        db.delete(data)
        db.commit()
        db.close()
        return {"Status": f"{id} berhasil dihapus"}
    else:
        return {"Status": f"{id} tidak ditemukan"}


@app.post("/product/", tags=['Product'])
def tambah_product(namaproduct: str, deskripsi: str, stok: int, harga: int):
    data = Product(nama=namaproduct, deskripsi=deskripsi,
                   stok=stok, harga=harga)
    db.add(data)
    db.commit()
    db.close()
    return {"status": "Ok", "Product": namaproduct, "deskripsi": deskripsi, "stok": stok, "harga": harga}


@app.delete("/product/{id}", tags=['Product'])
def hapus_product(id: int):
    data = db.query(Product).filter(Product.id == id).first()
    print(data)
    if data:
        db.delete(data)
        db.commit()
        db.close()
        return {"Status": f"{id} berhasil dihapus"}
    else:
        return {"Status": f"{id} tidak ditemukan"}


@app.put("/kategori/{id}", tags=['Kategori'])
def update_kategori(id: int, namakategori: str):
    data = db.query(Kategori).filter(Kategori.id == id).first()
    if data:
        data.nama = namakategori
        db.commit()
        db.close()
        return {"Status": f"{id} berhasil diubah"}
    else:
        return {"Status": f"{id} tidak ditemukan"}


@app.put("/product/{id}", tags=['Product'])
def update_produk(id: int, namaproduk: str, deskripsi: str, stok: int, harga: int):
    data = db.query(Product).filter(Product.id == id).first()
    if data:
        data.nama = namaproduk
        data.deskripsi = deskripsi
        data.stok = stok
        data.harga = harga
        db.commit()
        db.close()
        return {"status": f"{id} Berhasil diubah"}
    else:
        return {"status": f"{id} Tidak ditemukan"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
