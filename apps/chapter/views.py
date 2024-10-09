from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.firebase_storage import upload_to_firebase
from apps.book.models import Book
from apps.chapter.models import Chapter
from apps.chapter.serializers import ChapterSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Upload an mp3 file',
                    },
                    'id': {
                        'type': 'integer',  # Corrected the type to 'integer'
                        'description': 'Unique identifier for the file upload'  # Added a description
                    }
                },
                'required': ['file', 'id'],
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'url': {
                        'type': 'string',
                        'description': 'Public URL of the uploaded mp3 file'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message'
                    }
                }
            }
        },
    )
    def post(self, request, *args, **kwargs):
        # Check if a file is provided
        if 'file' not in request.FILES:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the file and its name
        file_obj = request.FILES['file']
        file_name = file_obj.name

        # Get the ID from the request data
        pk = request.data.get('id')

        # Ensure the ID corresponds to an existing Book
        subfolder = Book.objects.filter(pk=pk).only('isbn').first()
        if not subfolder:
            return Response({"error": "Book with provided ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Validate that the uploaded file is an mp3
        if not file_name.lower().endswith('.mp3'):
            return Response({"error": "Only mp3 files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Upload file to Firebase Storage and get the public URL
        public_url = upload_to_firebase(file_path=file_name, file_name=file_name, folder='audios',
                                        subfolder=subfolder.isbn)

        return Response({"url": public_url}, status=status.HTTP_200_OK)
