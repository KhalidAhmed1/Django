from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
    Relationship: OneToOne with Django's User model
    ManyToMany with Course (through enrollment)
    """
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['user__last_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} [{self.level}]"

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    def total_courses(self):
        return self.courses.count()