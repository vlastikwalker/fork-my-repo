import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

base_path = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(base_path / "templates"))

logging.basicConfig(filename='/var/log/bento/root_app.log',level=logging.DEBUG)
log = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
