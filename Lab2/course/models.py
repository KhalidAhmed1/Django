from django.db import models
from instructor.models import Instructor
from student.models import Student


class Course(models.Model):
    """
    Relationships:
    - ManyToOne  (ForeignKey) → Instructor  [One instructor teaches many courses]
    - ManyToMany → Student                  [Many students enroll in many courses]
    - Image field for course thumbnail
    """
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('business', 'Business'),
        ('science', 'Science'),
        ('language', 'Language'),
        ('math', 'Mathematics'),
        ('other', 'Other'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    # Core fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(default=0, help_text='Total hours')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    # Image field (requires Pillow)
    image = models.ImageField(
        upload_to='course_images/',
        null=True,
        blank=True,
        help_text='Course thumbnail image'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # ── RELATIONSHIPS ──────────────────────────────────────────────
    # ManyToOne (ForeignKey): One Instructor → Many Courses
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'   # instructor.courses.all()
    )

    # ManyToMany: Many Students ↔ Many Courses
    students = models.ManyToManyField(
        Student,
        blank=True,
        related_name='courses'   # student.courses.all()
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title

    def total_students(self):
        return self.students.count()

    def image_url(self):
        if self.image:
            return self.image.url
        return None