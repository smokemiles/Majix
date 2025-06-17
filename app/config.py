import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.urandom(32).hex())
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32).hex())
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    
    DATABASE_URL = os.getenv("DATABASE_URL")

    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}