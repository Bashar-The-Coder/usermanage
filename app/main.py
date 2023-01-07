from app.routers import  usersRoute , todosRoute
from fastapi import FastAPI
from .database import engine, Base
from . import models
# import models

description = """
TODO  API helps you do awesome stuff. 🚀

## Users

You can **read items**.

## Todo

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Todo - APP",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)


# models.Base.metadata.create_all(bind= engine)

models.Base.metadata.create_all(bind = engine)

app.include_router(usersRoute.router)
app.include_router(todosRoute.router)

