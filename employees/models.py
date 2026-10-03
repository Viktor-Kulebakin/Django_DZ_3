import os
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    # Расширение типовой пользовательской модели Django (OneToOneField)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Пользователь"
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Отчество (при наличии)"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Пол"
    )
    # Связь "многие ко многим" через промежуточную таблицу для хранения уровней освоения
    skills = models.ManyToManyField(
        'Skill',
        through='EmployeeSkill',
        verbose_name="Навыки"
    )
    # WYSIWYG-редактор на базе CKEditor
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    # Уровень освоения навыка строго от 1 до 10
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень освоения (1-10)"
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        unique_together = ('employee', 'skill')

    def __str__(self):
        return f"{self.skill.name} ({self.level})"


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        EmployeeProfile, 
        on_delete=models.CASCADE, 
        related_name='images', 
        verbose_name="Сотрудник"
    )
    image = models.ImageField(
        upload_to='employee_gallery/', 
        verbose_name="Изображение"
    )
    position = models.PositiveIntegerField(
        default=1, 
        verbose_name="Порядковый номер"
    )

    class Meta:
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Галерея изображений"
        ordering = ['position', 'id']

    def __str__(self):
        return f"Фото {self.position} для {self.employee.last_name}"


# Автоматическое физическое удаление файлов картинок с диска
@receiver(post_delete, sender=EmployeeImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
