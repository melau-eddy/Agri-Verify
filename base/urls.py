from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('verify/', views.verification_page, name='verification_page'),
    path('verify/qr/', views.verify_qr_code, name='verify_qr_code'),  # For QR code verification
    path('filter-products/', views.filter_products, name='filter_products'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('chat/api/', views.chat_api, name='chat_api'),
    path('webinars/', views.webinar_redirect, name='webinars'),
    path('quiz/', views.quiz, name='quiz'),
    path('products/<int:product_id>/qr/', views.qr_code_display, name='qr_code_display'),

    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('verify-product/', views.verify_product, name='verify_product'),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             email_template_name='password_reset_email.html',
             subject_template_name='password_reset_subject.txt',
             html_email_template_name='password_reset_email.html'  # Optional: for HTML emails
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ), 
         name='password_reset_complete'),

]