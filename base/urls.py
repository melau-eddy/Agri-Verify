from django.urls import path
from .views import chat_api, chat_view

urlpatterns = [
    path('agriculture-chat/', chat_view, name='agriculture_chat'),
    path('api/agriculture-chat/', chat_api, name='agriculture_chat_api'),
]