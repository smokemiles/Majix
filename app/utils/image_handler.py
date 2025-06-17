import uuid

from flask import current_app
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage

from app.config import Config

# Configure Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True
)

class ImageHandler:

    @staticmethod
    def allow_file(filename):
        return (
            '.' in filename and
            filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def upload_to_cloudinary(file, folder):
        """
        Uploads an image file to Cloudinary and returns the URL.
        """
        if not file or not ImageHandler.allow_file(file.filename):
            raise ValueError("Invalid file type or no file provided.")

        try:
            # Generate a unique filename
            unique_filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"

            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file,
                folder=folder,
                public_id=unique_filename,
                unique_filename=True,
                overwrite=True,
                resource_type="image"
            )

            # Get the secure URL of the uploaded image
            image_url = upload_result.get("secure_url")

            # Create a thumbnail URL
            thumbnail_url = CloudinaryImage(f"{folder}/{unique_filename}").build_url(
                width=150,
                height=150,
                crop="fill",
            )

            return {
                "original_url": image_url,
                "thumbnail_url": thumbnail_url,
                "public_id": upload_result.get("public_id"),
            }
        

        except Exception as e:
            current_app.logger.error(f"Error uploading image to Cloudinary: {str(e)}")
            raise ValueError("Failed to upload image to Cloudinary.") from e

