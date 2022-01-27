import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

logging.basicConfig(filename='/var/log/bento/hello_world.log',level=logging.DEBUG)
log = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("hello_world.html", {"request": {}, "id": 99})

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("hello_world.html", {"request": request, "id": id})

