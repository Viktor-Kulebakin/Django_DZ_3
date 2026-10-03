from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import EmployeeProfile

def index_view(request):
    """Главная страница: описание проекта и карточки сотрудников."""
    employees = EmployeeProfile.objects.all()
    context = {'title': 'Главная страница', 'employees': employees}
    return render(request, 'employees/index.html', context)

def employee_list_view(request):
    """Список всех сотрудников."""
    employees = EmployeeProfile.objects.all()
    context = {'title': 'Список сотрудников', 'employees': employees}
    return render(request, 'employees/list.html', context)

@login_required
def employee_detail_view(request, pk):
    """Подробная карточка сотрудника (только для авторизованных)."""
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    skills = employee.employeeskill_set.all()
    images = employee.images.all()
    context = {'employee': employee, 'skills': skills, 'images': images}
    return render(request, 'employees/detail.html', context)

def logout_view(request):
    """Кастомное представление для безопасного выхода пользователя."""
    logout(request)
    return redirect('employees:index')
