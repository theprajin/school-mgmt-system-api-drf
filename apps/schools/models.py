from django.db import models


class School(models.Model):

    name = models.CharField(max_length=255)
    max_students = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
