from django.urls import path, include
from rest_framework import routers

from .views import (CountryAPIView, CityRegionAPIView, AddressAPIView,
                    SpecialtyAPIView, LevelAPIView, TeacherAPIView,
                    SpecialtyLevelAPIView, StudentAPIView)


router = routers.SimpleRouter()
router.register('country', CountryAPIView)
router.register('city-region', CityRegionAPIView)
router.register('address', AddressAPIView)
router.register('specialty', SpecialtyAPIView)
router.register('level', LevelAPIView)
router.register('teacher', TeacherAPIView)
router.register('specialty-level', SpecialtyLevelAPIView)
router.register('student', StudentAPIView)


urlpatterns = [
    path('', include(router.urls))
]