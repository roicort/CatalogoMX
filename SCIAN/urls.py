from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'scian', views.ScianViewSet)

# Path: CATAMX/scian/views.py