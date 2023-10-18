from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base, engine
# from datetime import datetime
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    deskripsi = Column(String(256), nullable=False, default='-')
    stok = Column(Integer, default=0)
    harga = Column(Integer, default=0)

    gambar = relationship("Gambar", backref="produk")

    def __repr__(self):
        return f"<produk(nama='{self.nama}')>"


class Gambar(Base):
    __tablename__ = "gambar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idProduk = Column(Integer, ForeignKey(
        "product.id", ondelete="cascade"), nullable=False)
    file = Column(String(50), default='img-pruduct.jpg')


class Kategori(Base):
    __tablename__ = "kategori"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(50), nullable=False, index=True, unique=True)

    def __repr__(self):
        return f"<Kategori(nama='{self.nama}')>"


class ProductKategori(Base):
    __tablename__ = "kategoriproduct"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idproduct = Column(Integer, ForeignKey(
        "product.id", ondelete="cascade"), nullable=False)
    idkategori = Column(Integer, ForeignKey(
        "kategori.id", ondelete="cascade"), nullable=False)

    def __init__(self, idproduct, idkategori):
        self.idproduct = idproduct
        self.idkategori = idkategori


if __name__ == "__main__":
    Base.metadata.create_all(engine)
