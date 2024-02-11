from fastapi import Response
from fastapi import APIRouter
from generic_email_service.schemas import GESSchema
from generic_email_service.controllers import GESController

ges_router = APIRouter(prefix="/api")

@ges_router.post("/generic-email-service")
async def generic_email_service(email: GESSchema,response: Response):
    return await GESController.send_email(email,response)