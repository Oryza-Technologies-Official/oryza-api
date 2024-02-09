from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email_address: str
