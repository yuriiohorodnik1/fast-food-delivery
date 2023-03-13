import uvicorn
from fastapi import FastAPI


from api.routers.users import router as user_router
from api.routers.auth import router as login_router
from config.database import Base, engine

app = FastAPI(title="Fast Food delivery",
              description="Like a Bold Food, but better.",
              version="0.1.0",
              debug=True)

Base.metadata.create_all(bind=engine)

PATH_PREFIX_v1 = '/api/v1'

app.include_router(user_router, prefix=PATH_PREFIX_v1)
app.include_router(login_router, prefix=PATH_PREFIX_v1)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=4444)
