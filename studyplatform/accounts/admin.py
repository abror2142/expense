from django.contrib import admin

from .models import Country, CityRegion, Address, Specialty, Level, Teacher, SpecialtyLevel, Student


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(CityRegion)
class CityRegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region', 'country']
    list_display_links = ['name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'city_region', 'street']
    list_display_links = ['id']


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name']
    list_display_links = ['user']


@admin.register(SpecialtyLevel)
class SpecialtyLevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'specialty', 'teacher']
    list_display_links = ['id']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name']
    list_display_links = ['user']