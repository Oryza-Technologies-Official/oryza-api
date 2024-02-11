import os
import logging
from fastapi import status,Response
from fastapi.encoders import jsonable_encoder
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from dotenv import load_dotenv
from generic_email_service.schemas import GESSchema

load_dotenv()
LOG_FILE_PATH = os.path.join(os.getcwd(),"logs","ges_logs","ges.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename=LOG_FILE_PATH,mode="a")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)    
logger.addHandler(fh)

class GESController():
    def __init__():
        pass
    
    @staticmethod
    async def send_email(email: GESSchema,response: Response):
        try:
            conf = ConnectionConfig(
                MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
                MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
                MAIL_FROM = os.getenv("MAIL_FROM"),
                MAIL_PORT = os.getenv("MAIL_PORT"),
                MAIL_SERVER = os.getenv("MAIL_SERVER"),
                MAIL_STARTTLS = os.getenv("MAIL_STARTTLS"),
                MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS"),
                USE_CREDENTIALS = os.getenv("USE_CREDENTIALS"),
                VALIDATE_CERTS = os.getenv("VALIDATE_CERTS")
            )
            message = MessageSchema(
                        recipients = email.to,
                        cc = email.cc,
                        bcc = email.bcc,
                        subject = email.subject,
                        body = email.body,
                        attachments = email.attachments,
                        subtype="html"
                    )
            fm = FastMail(conf)
            await fm.send_message(message)
            logger.info(f"Email has been sent successfully to: {email.to} - cc: {email.cc} - bcc: {email.bcc} - subject: {email.subject} - No. of attachments: {len(email.attachments)}")
            response.status_code = status.HTTP_200_OK
            return jsonable_encoder({ "msg": "Email has been sent successfully", "status": status.HTTP_200_OK })
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            logger.error(str(err))
            return jsonable_encoder({ "error": str(err), "status": status.HTTP_400_BAD_REQUEST })