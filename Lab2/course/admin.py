from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display   = ['title', 'instructor', 'category', 'level', 'price', 'total_students', 'is_active']
    list_filter    = ['category', 'level', 'is_active']
    search_fields  = ['title', 'description']
    filter_horizontal = ['students']

    def total_students(self, obj):
        return obj.total_students()
    total_students.short_description = '# Students'