from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    """
    Relationship: OneToOne with Django's built-in User model
    An Instructor has exactly one User account and vice versa.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile'
    )
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    hire_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['user__last_name']
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.expertise})"

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    def total_courses(self):
        return self.courses.count()