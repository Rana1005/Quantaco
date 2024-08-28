from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializers import CustomerSerializer
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from .models import Customer

class UserRegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            password = data.get("password")
            confirm_password = data.pop("confirm_password", None)
            
            if password != confirm_password:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Passwords do not match."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            data["password"] = make_password(password)
            
            serializer = CustomerSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": status.HTTP_201_CREATED,
                    "message": "User registered successfully"
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as ve:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation error occurred.",
                "errors": str(ve)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError as ie:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Integrity error occurred. This might be due to a duplicate entry.",
                "errors": str(ie)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An unexpected error occurred.",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token is None:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Refresh token is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "status": status.HTTP_205_RESET_CONTENT,
                "message": "Logout successful."
            }, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid refresh token or token already blacklisted.",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class CustomerDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id

        customer_details = Customer.objects.filter(id=user_id).values(
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth'
        ).first()

        if not customer_details:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Customer not found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "Customer details fetched successfully.",
            "customer_details": customer_details
        }, status=status.HTTP_200_OK)
