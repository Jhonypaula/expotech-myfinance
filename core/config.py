from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
