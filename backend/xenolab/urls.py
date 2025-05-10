"""
URL configuration for xenolab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from wind.views import wind_data
from sunlight.views import sunlight_data
from temphumidity.views import temphumidity_data
from camera.views import camera_stream, camera_frame, camera_status, camera_control
from xenolab.views import get_lifeform_data, map_png

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wind/', wind_data, name='wind_data'),
    path('sunlight/', sunlight_data, name='sunlight_data'),
    path('temphumidity/', temphumidity_data, name='temphumidity_data'),
    
    # Camera endpoints
    path('camera/stream/<int:camera_id>/', camera_stream, name='camera_stream'),
    path('camera/stream/', camera_stream, name='default_camera_stream'),  # Default camera
    path('camera/frame/<int:camera_id>/', camera_frame, name='camera_frame'),
    path('camera/frame/', camera_frame, name='default_camera_frame'),  # Default camera
    path('camera/status/<int:camera_id>/', camera_status, name='camera_status'),
    path('camera/status/', camera_status, name='default_camera_status'),  # Default camera
    path('camera/control/<int:camera_id>/', camera_control, name='camera_control'),
    path('camera/control/', camera_control, name='default_camera_control'),  # Default camera
    
    # Xenolab endpoints
    path('lifeform/', get_lifeform_data, name='get_lifeform_data'),
    path('map/', map_png, name='map_png'),
]
