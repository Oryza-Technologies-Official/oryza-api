from fastapi import Response
from fastapi import APIRouter
from green_guard_service.schemas import ImageFileSchema
from green_guard_service.controllers import GGSController

ggs_router = APIRouter(prefix="/oryza/api")

@ggs_router.post("/green-guard-service/disease-summary")
async def green_guard_service(image_file: ImageFileSchema,response: Response):
    return GGSController.generate_disease_summary(image_file,response)