from typing import Optional

from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"


settings = Settings()

app = FastAPI(openapi_url=settings.openapi_url)


@app.get("/", name="index")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id:int}")
def read_item(item_id: int, q: Optional[int] = None):
    return {"item_id": item_id, "q": q}
