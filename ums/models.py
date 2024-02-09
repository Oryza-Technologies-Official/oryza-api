from sqlalchemy import Column, String
from sqlalchemy_utils import EmailType
from db_config import Base

class User(Base):
   
    __tablename__ = "user_profile_information"

    user_id = Column(String,nullable=False,primary_key=True)
    username = Column(String,nullable=False)
    email_address = Column(EmailType,nullable=False,unique=True)
    date_of_creation = Column(String,nullable=False)

