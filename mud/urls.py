from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'test', )
path('api/', include(router.urls))
