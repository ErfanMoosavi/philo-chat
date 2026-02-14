import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from .routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    app.state.openai_api_key = os.getenv("OPENAI_API_KEY")
    app.state.base_url = os.getenv("BASE_URL")
    app.state.model_name = os.getenv("MODEL_NAME")

    print("App startup")

    yield

    print("App shutdown")


app = FastAPI(
    title="Philo-Chat",
    description="Chat with your favorite philosophers - Nietzsche, Socrates, and more-in real-time!",
    contact={"name": "Erfan Moosavi", "email": "erfanmoosavi84@gmail.com"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.include_router(routers.router)


@app.get("/")
def root():
    return {"message": "Philosopher Chat API"}
