from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.requests import Request

from init.initialize import initialize
from tools.mongo import Mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    global mongo
    mongo = Mongo()
    yield

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO life probe, health check

@app.get("/search")
def get_method(request: Request):
    logger.info("Search request")
    filters = dict(request.query_params)
    if "keywords" in filters.keys():
        keywords = filters["keywords"]
        response = mongo.search(keywords, filters)
        logger.info(f"Returned {len(response)} amendments")
        return response
    else:
        return Mongo.searchError("Missing keywords query parameter")


@app.post("/stats")
async def post_method():
    logger.info("Stats request")
    response = mongo.generate_stats()
    logger.info("Returned stats")
    return response


@app.get("/authors/{author_id}")
def get_method(author_id: str):
    logger.info("Author request")
    response = mongo.search_author(author_id)
    logger.info("Returned author")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)