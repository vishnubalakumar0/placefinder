from django.contrib import admin
from django.urls import path, include
import locationapp.urls
from locationapp.views import login_page
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from placefinder import settings

# ✅ Import Django's built-in auth views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('locationapp/', include('locationapp.urls')),
    path('', login_page, name="login_page"),

    # ✅ Password Reset URLs (Django default)
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
