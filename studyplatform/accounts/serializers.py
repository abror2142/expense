from rest_framework import serializers

from .models import Country, CityRegion, Address, Specialty, Level, Teacher, SpecialtyLevel, Student


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CityRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityRegion
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class SpecialtyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialtyLevel
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


