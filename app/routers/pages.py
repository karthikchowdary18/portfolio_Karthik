from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)

PROFILE = {
    "name": "Karthik Chowdary Nunna",
    "short_name": "Karthik",
    "location": "Kronach, Germany",
    "email": "karthikchowdarynunna@gmail.com",
    "phone": "+49 15563569114",
    "linkedin": "https://www.linkedin.com/in/karthik-chowdary-nunna/",
    "github": "https://github.com/karthikchowdary18",
}


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "title": "Karthik Chowdary Nunna | Portfolio",
            "meta_description": (
                "Premium bilingual portfolio for Karthik Chowdary Nunna covering autonomous "
                "driving, robotics software, human-machine interfaces, and digital systems."
            ),
            "profile": PROFILE,
        },
    )
