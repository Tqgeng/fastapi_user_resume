from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/resumes", response_class=HTMLResponse)
async def resumes_page(request: Request):
    return templates.TemplateResponse("resumes.html", {"request": request})


@router.get("/resumes/new", response_class=HTMLResponse)
async def resume_new_page(request: Request):
    return templates.TemplateResponse("resume_new.html", {"request": request})


@router.get("/resumes/{resume_id}", response_class=HTMLResponse)
async def resume_view_page(request: Request, resume_id: int):
    # Шаблон сам загрузит данные через JS
    return templates.TemplateResponse("resume_view.html", {"request": request})
