from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="")

@app.get("/")
def index(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})

@app.get("/kelas")
def weblanjut():
    return {"Nim :" "H071201064", "Kelas :" "Pemrograman Web Lanjutan" }

@app.get("/unhas/{nama}")
def unhas(nama: str):
    kuliah = ["Pemrograman Web Lanjut", "Visualisasi Informasi", "Etika Profesi"]
    return {"Nim": "H071201064", "Nama": nama, "Kuliah": kuliah }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)