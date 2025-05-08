from django.urls import path
from .views import chat_api, chat_view
from .import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('api/agriculture-chat/', chat_api, name='agriculture_chat_api'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('details/', views.details, name='details'),
    path('verify/', views.verify_product, name='verify_product'),
]