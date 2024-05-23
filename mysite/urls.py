"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from mysite import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import send_email
from django.contrib.auth import urls


urlpatterns = [
    path('admin/', admin.site.urls),
     path('generate/', views.generate_report, name='generate_report'),
     path('download_report/<int:report_id>/', views.download_report, name='download_report'),
     path('admin/logout/', views.admin_logout , name='admin_logout'),
    path('', views.homepage, name='homepage'),
    path('appointment/', views.appointment, name='appointment'),
    path('signup/', views.signup, name='signup'),
    path('login2/', views.loginpage, name='login2'),
     path('login/', views.login_view, name='login'),
    # path('login/', auth_views.LoginView.login_view(), name='login'),
    path('profile/', views.profile , name='profile'),
    path('view-appointments/', views.view_appointments, name='view_appointments'),
     path('aboutus/', views.aboutus, name='aboutus'),
      path('service/', views.services, name='service'),
    path('gallery/', views.Gallery, name='gallery'),
    path('logout_view/',views.logout_view,name='logout_view'),
    # path('login_view' , views.login_view , name='login_view'),
    path('servicedetails/<serviceid>',views.serviceDetails ),
    path('api/slots/', views.get_available_slots, name='get_available_slots'),
    path('send-email/', views.send_email, name='send_email'), 

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

