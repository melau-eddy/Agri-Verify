from django.urls import path
from .views import chat_api, chat_view
from .import views

urlpatterns = [
    path('', chat_view, name='agriculture_chat'),
    path('api/agriculture-chat/', chat_api, name='agriculture_chat_api'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
]