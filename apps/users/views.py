from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer

class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError({'password_mismatch': 'Password fields did not match.'})

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyAPIView(APIView):

    def post(self, request):
        email = request.data.get('email')
        print(email)

        if not email:
            raise ValidationError({'email': 'Email is required.'})
        
        # Here you would typically send a verification email
        # For demonstration, we will just return a success message
        return Response({'message': 'Verification email sent successfully.'}, status=status.HTTP_200_OK)