"""
URL configuration for the app.
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet


from Services import views


# Create a router and register the ViewSet with it
router = DefaultRouter()
router.register(r'farmers', FarmerViewSet)

urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('forgot_password/', views.forgot_password_view, name='forgot-password'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    
    path('registered_farmers/', views.registered_farmers, name='registered_farmers'),
   
     path('map/', views.map, name='map'),
      path('advisories/', views.advisories, name='advisories'),
    # Services
    
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('users/', views.users, name='users'),
    path('update_user/', views.update_user, name='update_user'),
    path('change-activity-status/', views.change_user_activity_status, name='change_user_activity_status'),
    
    path('buttons/', views.buttons, name='buttons'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('upload_file/', views.upload_file, name='upload_file'),
    
    # reset password routes
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form_.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done_.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm_.html",post_reset_login=True,  # Auto-login after password reset
         post_reset_login_backend='django.contrib.auth.backends.ModelBackend'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete_.html"),
         name="password_reset_complete"),
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),

#     path('api/expiry-notifications/', views.ExpiryNotificationsAPI.as_view(), name='expiry-notifications'),
     path('', include(router.urls)),
]
