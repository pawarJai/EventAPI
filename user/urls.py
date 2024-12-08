from django.urls import path
from .views import RegisterUser,LoginView,UserManagementView,UpdateUser

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('user/', UserManagementView.as_view(), name='user_management'),
    path('user/<pk>/', UpdateUser.as_view(), name='user_management'),

]
