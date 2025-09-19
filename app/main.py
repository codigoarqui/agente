from app.routes import agent
from fastapi import FastAPI
app = FastAPI()

app.include_router(agent.router, prefix="/agent")
