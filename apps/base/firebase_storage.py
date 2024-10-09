import mimetypes
from firebase_admin import storage

def upload_to_firebase(file_path, file_name, folder='audiobooks', subfolder=None):
    if subfolder is None:
        subfolder = 'others'

    try:
        bucket = storage.bucket()
        full_path = f"{folder}/{subfolder}/{file_name}"
        content_type, _ = mimetypes.guess_type(file_path)

        blob = bucket.blob(full_path)

        with open(file_path, 'rb') as file:
            blob.upload_from_file(file, content_type=content_type)

        blob.make_public()
        return blob.public_url

    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error uploading file: {str(e)}"
