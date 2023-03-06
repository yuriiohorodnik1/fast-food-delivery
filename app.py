from fastapi import FastAPI
from api.routers.users import router as user_router
from config.database import Base, engine

app = FastAPI(title="Fast Food delivery",
              description="Like a Bold Food, but better.",
              version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix='/api/v1')
