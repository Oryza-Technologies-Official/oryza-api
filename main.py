import ums
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ums.routes import ums_router
from generic_email_service.routes import ges_router
from green_guard_service.routes import ggs_router
from db_config import engine

ums.models.Base.metadata.create_all(bind=engine)
origins = [
    "*"
]
app = FastAPI()
app.include_router(ums_router)
app.include_router(ges_router)
app.include_router(ggs_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)