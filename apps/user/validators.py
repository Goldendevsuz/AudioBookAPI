from django.core.exceptions import ValidationError


def validate_image(image):
    try:
        file_size = image.size if hasattr(image, 'size') else len(image.read())
        limit_mb = 10  # Maximum file size in megabytes
        if file_size > limit_mb * 1024 * 1024:  # Convert MB to bytes
            raise ValidationError(f"Max size of file is {limit_mb} MB")
    except AttributeError:
        raise ValidationError("Invalid file. The uploaded file is not valid.")
    finally:
        # Reset file pointer to the beginning in case it's needed elsewhere
        image.seek(0)
