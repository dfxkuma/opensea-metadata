import os
import dataclasses

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from tortoise.contrib.fastapi import register_tortoise
from server.ratelimit import global_limiter

from model import SampleNFT


app = FastAPI(
    name="Opensea Metadata Server",
    docs_url=None,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state_limiter = global_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


register_tortoise(
    app=app,
    db_url="sqlite://data/db.sqlite3",
    modules={"models": ["model"]},
    generate_schemas=True,
)


@app.get("/api")
async def main(_request: Request):
    print("h")
    return HTMLResponse(content="<h1>Opensea Metadata Server</h1>", status_code=200)


@app.get("/api/image/{image_id}")
async def image(_request: Request, image_id: int):
    if os.path.exists(f"images/{str(image_id)}.png"):
        return FileResponse(
            path=f"images/{str(image_id)}.png",
            status_code=200,
            media_type="image/png",
            filename=f"{str(image_id)}.png",
        )
    else:
        return HTTPException(
            status_code=404, detail=f"Metadata image not found on #{str(image_id)}"
        )


@app.get("/api/metadata/{metadata_id}")
async def metadata(_request: Request, metadata_id: int):
    if not await SampleNFT.exists(id=int(metadata_id + 1)):
        return HTTPException(
            status_code=404,
            detail=f"Metadata not found on #{str(metadata_id)}",
        )
    else:
        model = await SampleNFT.get(id=int(metadata_id + 1))
        response = {
            "name": model.name,
            "description": model.description,
            "image": model.image,
        }
        if model.external_url:
            response["external_url"] = model.external_url
        if len(model.attributes) > 0:
            response["attributes"] = []
            for trait in model.attributes:
                response["attributes"].append(dataclasses.asdict(trait))
        return response
