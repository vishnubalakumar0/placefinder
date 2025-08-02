from django.urls import path
from locationapp import views
from .views import forgot_password, reset_password
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('homepage/', views.homepage, name="home-page"),
    path('register/', views.register, name="register"),
    path('shop/<int:shop_id>/map/', views.shop_map, name="shop_map"),
    path('place_visit/', views.place_visit, name="place_visit"),
    path('visit/', views.visit, name="visit"),
    path('speech_result/', views.speech_result, name="speech_result"),
    path('api/forgot-password/', views.forgot_password, name="forgot_password"),
    path('forgot/', views.forgot, name="forgot"),
    path('reset-password/<uidb64>/<token>/', views.reset, name="reset"),
    path('api/reset-password/<uidb64>/<token>/', views.reset_password, name="reset-password"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/homepage/'), name='logout')
]
