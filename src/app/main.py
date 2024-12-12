from fastapi import FastAPI
from .routers.authors import router_authors
from .routers.books import router_books
from .routers.borrows import router_borrows

app = FastAPI()


app.include_router(router_authors)
app.include_router(router_borrows)
app.include_router(router_books)
