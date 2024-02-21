import os
import uuid
import datetime
import logging
from fastapi import status,Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ums.schemas import UserSchema,UpdateUserSchema
from ums.models import User

LOG_FILE_PATH = os.path.join(os.getcwd(),"logs","ums_logs","ums.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=LOG_FILE_PATH,mode="a")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)    
logger.addHandler(fh)

class UserController():
    
    def __init__():
        pass
    
    @staticmethod
    def create_user(user: UserSchema,response: Response,db: Session):
        try:
            is_exists_username = db.query(User).filter(User.username == user.username).first()
            is_exists_email_address = db.query(User).filter(User.email_address == user.email_address).first()
            
            if is_exists_username:
                raise Exception("Username already exists")
            elif is_exists_email_address:
                raise Exception("Email address already exists")

            user_id = "ORZ-"+str(uuid.uuid4())
            date_of_creation = datetime.datetime.now().strftime("%Y-%m-%d")
            new_user = User(user_id=user_id,**user.dict(),date_of_creation=date_of_creation) 
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info("User has been created successfully")
            response.status_code = status.HTTP_201_CREATED
            return jsonable_encoder({ "msg": "User has been created successfully", "status": status.HTTP_201_CREATED })
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            logger.error(str(err))
            return jsonable_encoder({ "error": str(err), "status": status.HTTP_400_BAD_REQUEST })
    @staticmethod
    def update_user(user: UpdateUserSchema,response: Response,db: Session):
        try:
            user_id = user.user_id
            field_name = user.field_name
            new_value = user.new_value

            is_updated = db.query(User).filter(User.user_id == user_id).first()
            if is_updated:
                pass
        except Exception as err:
            response.status_code = status.HTTP_417_EXPECTATION_FAILED
            logger.error(str(err))
            return jsonable_encoder({ "error": str(err), "status": status.HTTP_417_EXPECTATION_FAILED })

