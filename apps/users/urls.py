from django.urls import path
from  . views import SignupAPIView,VerifyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView,TokenRefreshView


app_name = 'apps.users'


urlpatterns = [
     path('signup/', SignupAPIView.as_view(), name='signup'),
     path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path('verify-email/', VerifyAPIView.as_view(), name='verify_email'),
]