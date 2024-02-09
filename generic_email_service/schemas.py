from pydantic import BaseModel
from typing import List

class GESSchema(BaseModel):
    to: List[str]
    cc: List[str] = []
    bcc: List[str] = []
    subject: str
    body: str
    attachments: List[str] = []
