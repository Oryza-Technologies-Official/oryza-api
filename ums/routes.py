from fastapi import APIRouter,Depends,Response
from sqlalchemy.orm import Session
from ums.schemas import UserSchema,UpdateUserSchema
from ums.controllers import UserController
from db_config import get_db

ums_router = APIRouter(prefix="/api")

@ums_router.post("/create-user")
async def create_user(user: UserSchema,response: Response,db: Session = Depends(get_db)):
    return UserController.create_user(user,response,db)

@ums_router.post("/update-user")
async def update_user(user: UpdateUserSchema,response: Response,db: Session = Depends(get_db)):
    pass
