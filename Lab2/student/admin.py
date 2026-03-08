from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['get_full_name', 'level', 'phone', 'enrollment_date', 'total_courses']
    list_filter   = ['level', 'enrollment_date']
    search_fields = ['user__first_name', 'user__last_name']

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'

    def total_courses(self, obj):
        return obj.total_courses()
    total_courses.short_description = '# Courses'