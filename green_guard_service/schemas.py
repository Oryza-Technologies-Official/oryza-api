from pydantic import BaseModel

class ImageFileSchema(BaseModel):
    image_file_base64_str: str