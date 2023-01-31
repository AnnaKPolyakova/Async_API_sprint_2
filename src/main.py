import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, person
from core.config import settings
from db import elastic, redis

app = FastAPI(
    title=settings["PROJECT_NAME"],
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    url = settings["REDIS_PROTOCOL"] + "://" + settings["REDIS_HOST"]
    redis.redis = await aioredis.from_url(url)
    elastic.es = AsyncElasticsearch(
        hosts=[f"{settings['ELASTIC_HOST']}:{settings['ELASTIC_PORT']}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(person.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
