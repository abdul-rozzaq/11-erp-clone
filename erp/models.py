from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role = models.CharField(
        choices=(
            ("not_assigned", "Tayinlanmagan"),
            ("teacher", "O'qituvchi"),
            ("student", "Talaba"),
            ("admin", "Admin"),
        ),
        default="not_assigned",
        max_length=128,
    )

    def __str__(self) -> str:
        return self.get_full_name()


class Course(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    title = models.CharField(max_length=128)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teacher_groups"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    students = models.ManyToManyField(User, blank=True, related_name="student_groups")

    days = models.ManyToManyField(Day)
    status = models.CharField(
        choices=(
            ("active", "Faol"),
            ("inactive", "Faol emas"),
        ),
        default="active",
        max_length=10,
    )

    def formatted_start_time(self):
        return self.start_time.strftime("%H:%M")

    def formatted_end_time(self):
        return self.end_time.strftime("%H:%M")
