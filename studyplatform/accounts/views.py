from rest_framework import viewsets

from .models import (Country, CityRegion, Address, Specialty, Level,
                     Teacher, SpecialtyLevel, Student)
from .serializers import (CountrySerializer, CityRegionSerializer,
                          AddressSerializer, SpecialtySerializer,
                          LevelSerializer, TeacherSerializer,
                          SpecialtyLevelSerializer, StudentSerializer)

class CountryAPIView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityRegionAPIView(viewsets.ModelViewSet):
    queryset = CityRegion.objects.all()
    serializer_class = CityRegionSerializer


class AddressAPIView(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class SpecialtyAPIView(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class LevelAPIView(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class TeacherAPIView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SpecialtyLevelAPIView(viewsets.ModelViewSet):
    queryset = SpecialtyLevel.objects.all()
    serializer_class = SpecialtyLevelSerializer


class StudentAPIView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class LevelAPIView(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
