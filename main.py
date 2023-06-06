from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users


app = FastAPI()


#ROUTES
app.include_router(users.router)

#Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

