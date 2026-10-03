from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import EmployeeProfile, EmployeeImage, Skill, EmployeeSkill


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1
    fields = ['image', 'position']
    ordering = ['position']


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'gender')
    inlines = [EmployeeSkillInline, EmployeeImageInline]


# Переименование встроенных моделей в админке для красоты
Group._meta.verbose_name = 'Группа'
Group._meta.verbose_name_plural = 'Группы'
User._meta.verbose_name = 'Пользователь'
User._meta.verbose_name_plural = 'Пользователи'
