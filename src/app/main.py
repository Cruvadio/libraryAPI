from fastapi import FastAPI
from .authors import router_authors

app = FastAPI()


app.include_router(router_authors)
