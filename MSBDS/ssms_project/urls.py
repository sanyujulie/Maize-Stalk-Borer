"""
URL configuration for ssms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from Services import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Services.urls')),
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
     path('images/', views.images, name='images'),
    path('buttons/', views.buttons, name='buttons'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
  
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
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
    

#     path('api/expiry-notifications/', views.ExpiryNotificationsAPI.as_view(), name='expiry-notifications'),
     path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'Services.views.handle_404'  #page_not_found
