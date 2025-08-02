from django.urls import path
from django.urls import path
from locationapp import views
from .views import (
    forgot_password, 
    reset_password,
    homepage,
    register,
    shop_map,
    place_visit,
    visit,
    speech_result,
    forgot,
    reset,
    listings_view,  # New import
    contact_view    # New import
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Main pages
    path('', homepage, name="home"),
    path('homepage/', homepage, name="home-page"),
    
    # User authentication
    path('register/', register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='locationapp/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Password management
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='locationapp/password_reset.html'),
         name="password_reset"),
    path('api/forgot-password/', forgot_password, name="forgot_password"),
    path('forgot/', forgot, name="forgot"),
    path('reset-password/<uidb64>/<token>/', reset, name="reset"),
    path('api/reset-password/<uidb64>/<token>/', reset_password, name="reset-password"),
    
    # Business listings
    path('listings/', listings_view, name="listings"),  # More Cities page
    path('shop/<int:shop_id>/map/', shop_map, name="shop_map"),
    
    # User activities
    path('place_visit/', place_visit, name="place_visit"),
    path('visit/', visit, name="visit"),
    
    # Special features
    path('speech_result/', speech_result, name="speech_result"),
    
    # Contact page
    path('contact/', contact_view, name="contact"),
]