from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email_address: str

class UpdateUserSchema(BaseModel):
    user_id: str
    field_name: str
    new_value: str