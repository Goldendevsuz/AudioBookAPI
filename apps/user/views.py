import random

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from icecream import ic
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from .emails import CustomActivationEmail, generate_activation_code
from .models import UserCategory, UserBook
from .serializers import UserCategorySerializer, UserBookSerializer, CustomTokenCreateSerializer, \
    CustomActivationSerializer

User = get_user_model()


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', location=OpenApiParameter.PATH, required=True, type=int)
    ]
)
class UserCategoryViewSet(viewsets.ModelViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserCategory.objects.filter(user_id=user_id)


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', location=OpenApiParameter.PATH, required=True, type=int),
    ]
)
class UserBookViewSet(viewsets.ModelViewSet):
    queryset = UserBook.objects.all()
    serializer_class = UserBookSerializer
    search_fields = ['book__title', 'book__author__name']  # Fields to search

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = UserBook.objects.filter(user_id=user_id)

        # You can further customize the queryset here
        return queryset


class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Custom Token Response",
                examples={
                    'application/json': {
                        'refresh': 'refresh-token-example',
                        'access': 'access-token-example',
                        'user': {
                            'id': 1,
                            'username': 'uznext',
                            'email': 'uznext17@gmail.com',
                        },
                        'remember_me': False
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class CustomUserViewSet(UserViewSet):
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance # noqa
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            ic(f"Image type: {type(image_file)}")
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Custom logic for deleting the user
        instance = self.get_object()

        # Check if the user is a superuser
        if request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            # Perform the deletion
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Return a permission denied response for non-superusers
        return Response(
            data={
                "detail": "You don't have permission to delete this profile."
            },
            status=status.HTTP_403_FORBIDDEN
        )


class CustomActivationView(viewsets.GenericViewSet):
    serializer_class = CustomActivationSerializer

    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            # Use get() to retrieve a single user object, not filter()
            user = User.objects.get(email=email, is_active=False)

            # Generate and send the activation code via email
            sent_code = generate_activation_code()
            send_activation_email(user, sent_code)

            # Validate the code provided by the user
            if code == sent_code:
                user.is_active = True
                user.save()
                return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "Invalid email or user already activated."}, status=status.HTTP_404_NOT_FOUND)