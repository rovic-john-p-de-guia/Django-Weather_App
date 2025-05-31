from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProtectedView, login_view, register_view, custom_logout_view

urlpatterns = [
    # Template-based URLs
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', custom_logout_view, name='logout'),
    
    # API URLs
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
] 