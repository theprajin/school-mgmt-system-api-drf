from django.db import models
from apps.schools.models import School


class Student(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="students",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        app_label = "students"
