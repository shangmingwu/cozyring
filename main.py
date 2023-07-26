import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from random import randint
import json

# Load the sites in the webring.

with open("sites.json", "r") as fp:
    raw = fp.read()

sites = json.loads(raw)["sites"]

index = {}

for i in range(0, len(sites)):
    slug = sites[i]["slug"]
    index[slug] = i

# Disable the documentation.

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", name="root")
async def root(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request, "sites": sites})

@app.get("/inst/", name="instructions_list")
async def list_inst(request: Request):
    return templates.TemplateResponse("instructions_list.html", {"request": request, "sites": sites})

@app.get("/inst/{slug}", name="instructions")
async def get_inst(slug: str, request: Request):
    if not slug in index:
        raise HTTPException(status_code=404, detail="Invalid webring slug.")
    n = index[slug]
    url = sites[n]["url"]
    name = sites[n]["name"]
    return templates.TemplateResponse("instructions.html", {"request": request, "slug_passed": slug, "url": url, "name": name})

@app.get("/next/{slug}", name="next")
async def get_next(slug: str):
    if len(sites) == 0:
        raise HTTPException(status_code=404, detail="No sites in webring.")
    if not slug in index:
        raise HTTPException(status_code=404, detail="Invalid webring slug.")
    n = (index[slug] + 1) % (len(sites))
    url = sites[n]["url"]
    return RedirectResponse(url)

@app.get("/prev/{slug}", name="previous")
async def get_prev(slug: str):
    if len(sites) == 0:
        raise HTTPException(status_code=404, detail="No sites in webring.")
    if not slug in index:
        raise HTTPException(status_code=404, detail="Invalid webring slug.")
    n = (index[slug] - 1) % (len(sites))
    url = sites[n]["url"]
    return RedirectResponse(url)

@app.get("/random", name="random")
async def get_random():
    if len(sites) == 0:
        raise HTTPException(status_code=404, detail="No sites in webring.")
    n = randint(0, len(sites) - 1)
    url = sites[n]["url"]
    return RedirectResponse(url)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("error.html", {"request": request, "status_code": str(exc.status_code), "detail": str(exc.detail)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
