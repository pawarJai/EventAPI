from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.helper import IsAdminUser




class LoginView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Login and get JWT tokens (access & refresh) for a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User's password")
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="JWT tokens returned successfully.",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string",
                    }
                }
            ),
            400: "Bad Request - Missing credentials",
            401: "Unauthorized - Invalid credentials"
        }
    )
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED

            )
            
            
class RegisterUser(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="User's username"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="User's first_name"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="User's last_name"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description="User's role"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User's password")
            },
            required=['username','first_name','last_name','email','role', 'password']
        ),
        responses={
            201: UserSerializer,
            400: "Bad Request - Invalid data"
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManagementView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]
    @swagger_auto_schema(
        operation_description="Get a list of all users",
        responses={
            200: UserSerializer(many=True),
            400: "Bad Request"
        }
    )
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    @swagger_auto_schema(
        operation_description="Update a specific user's data by ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="User's username"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="User's first_name"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="User's last_name"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
                'role': openapi.Schema(type=openapi.TYPE_STRING, description="User's role"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User's password")
            },
            required=['username','first_name','last_name','email','role', 'password']
        ),
        responses={
            200: UserSerializer,
            400: "Bad Request - Invalid data",
            403: "Forbidden - You do not have permission to update this user",
            404: "Not Found - User does not exist"
        }
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != user:
            return Response(
                {"detail": "You do not have permission to update this user."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
