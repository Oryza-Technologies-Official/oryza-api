import os
import logging
import pybase64
import shutil
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from fastapi import status,Response
from fastapi.encoders import jsonable_encoder
from green_guard_service.schemas import ImageFileSchema

LOG_FILE_PATH = os.path.join(os.getcwd(),"logs","ggs_logs","ggs.log")
TEMP_IMAGE_STORAGE_DIR_PATH = os.path.join(os.getcwd(),"green_guard_service","temp_image_storage")
AI_MODEL_FILE_PATH = os.path.join(os.getcwd(),"trained_ai_models","resnet18classification_model.pth")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=LOG_FILE_PATH,mode="a")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)    
logger.addHandler(fh)

class GGSController():
    def __init__():
        pass

    def generate_disease_summary(image_file: ImageFileSchema,response: Response):
        try:
            os.makedirs(TEMP_IMAGE_STORAGE_DIR_PATH,exist_ok=True)
            with open(os.path.join(TEMP_IMAGE_STORAGE_DIR_PATH,"test_image.png"),"wb") as ifh:
                ifh.write(pybase64.b64decode((image_file.image_file_base64_str)))
            
            model = models.resnet18(pretrained=True)
            model.fc = nn.Linear(model.fc.in_features,1000)
            model.load_state_dict(torch.load(AI_MODEL_FILE_PATH))
            model.eval()
            new_model = models.resnet18(pretrained=True)
            new_model.fc = nn.Linear(new_model.fc.in_features, 38)
            new_model.fc.weight.data = model.fc.weight.data[0:38] 
            new_model.fc.bias.data = model.fc.bias.data[0:38]

            image_path = os.path.join(TEMP_IMAGE_STORAGE_DIR_PATH,"test_image.png")
            image = Image.open(image_path)
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            input_tensor = preprocess(image)
            input_batch = input_tensor.unsqueeze(0) 
            with torch.no_grad():
                output = model(input_batch)

            _, predicted_class = output.max(1)

            class_names = ["Apple___Apple_scab","Apple___Black_rot","Apple___Cedar_apple_rust","Apple___healthy",
                           "Blueberry___healthy","Cherry_(including_sour)___Powdery_mildew","Cherry_(including_sour)___healthy","Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
                           "Corn_(maize)___Common_rust_","Corn_(maize)___Northern_Leaf_Blight","Corn_(maize)___healthy","Grape___Black_rot",
                           "Grape___Esca_(Black_Measles)","Grape___Leaf_blight_(Isariopsis_Leaf_Spot)","Grape___healthy","Orange___Haunglongbing_(Citrus_greening)",
                           "Peach___Bacterial_spot","Peach___healthy","Pepper,_bell___Bacterial_spot","Pepper,_bell___healthy",
                           "Potato___Early_blight","Potato___Late_blight","Potato___healthy","Raspberry___healthy","Soybean___healthy",
                           "Squash___Powdery_mildew","Strawberry___Leaf_scorch","Strawberry___healthy","Tomato___Bacterial_spot",
                           "Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Spider_mites Two-spotted_spider_mite",
                           "Tomato___Target_Spot","Tomato___Tomato_Yellow_Leaf_Curl_Virus","Tomato___Tomato_mosaic_virus","Tomato___healthy"
                          ]

            predicted_disease_summary = class_names[predicted_class.item()].split("___")
            plant_name = predicted_disease_summary[0]
            disease_status = "Unhealhty" if predicted_disease_summary[1] != "healhty" else "Healhty"
            disease_name = predicted_disease_summary[1]

            shutil.rmtree(TEMP_IMAGE_STORAGE_DIR_PATH)
            logger.info("Generated disease summary")
            response.status_code =  status.HTTP_200_OK
            return jsonable_encoder({ "msg": { "plant_name": plant_name,"disease_status": disease_status, "disease_name": disease_name }, "status": status.HTTP_200_OK })
        except Exception as err:
            shutil.rmtree(TEMP_IMAGE_STORAGE_DIR_PATH)
            logger.error(str(err))
            response.status_code = status.HTTP_400_BAD_REQUEST
            return jsonable_encoder({ "error": str(err), "status": status.HTTP_400_BAD_REQUEST })
