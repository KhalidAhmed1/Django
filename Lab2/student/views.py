from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student


def student_list(request):
    """List all students."""
    students = Student.objects.select_related('user').all()
    return render(request, 'student/student_list.html', {
        'students': students,
        'page_title': 'All Students',
    })


def student_detail(request, pk):
    """Show a single student and their enrolled courses."""
    student = get_object_or_404(Student.objects.select_related('user'), pk=pk)
    enrolled_courses = student.courses.filter(is_active=True).select_related('instructor__user')
    return render(request, 'student/student_detail.html', {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'page_title': student.get_full_name(),
    })


def student_create(request):
    """Create a new student."""
    if request.method == 'POST':
        first_name    = request.POST.get('first_name', '').strip()
        last_name     = request.POST.get('last_name', '').strip()
        email         = request.POST.get('email', '').strip()
        level         = request.POST.get('level', 'beginner')
        phone         = request.POST.get('phone', '').strip()
        date_of_birth = request.POST.get('date_of_birth') or None

        if not (first_name and last_name and email):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'student/student_form.html', {
                'page_title': 'Add Student',
                'form_data': request.POST,
                'level_choices': Student.LEVEL_CHOICES,
            })

        username = f"stu.{first_name.lower()}.{last_name.lower()}"
        base, counter = username, 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password='changeme123'
        )
        Student.objects.create(
            user=user,
            level=level,
            phone=phone,
            date_of_birth=date_of_birth,
        )
        messages.success(request, f'Student {user.get_full_name()} enrolled!')
        return redirect('student_list')

    return render(request, 'student/student_form.html', {
        'page_title': 'Add Student',
        'level_choices': Student.LEVEL_CHOICES,
    })


def student_edit(request, pk):
    """Edit an existing student."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.user.first_name = request.POST.get('first_name', '').strip()
        student.user.last_name  = request.POST.get('last_name', '').strip()
        student.user.email      = request.POST.get('email', '').strip()
        student.level           = request.POST.get('level', 'beginner')
        student.phone           = request.POST.get('phone', '').strip()
        student.date_of_birth   = request.POST.get('date_of_birth') or None
        student.user.save()
        student.save()
        messages.success(request, 'Student updated!')
        return redirect('student_detail', pk=pk)

    return render(request, 'student/student_form.html', {
        'student': student,
        'page_title': f'Edit {student.get_full_name()}',
        'level_choices': Student.LEVEL_CHOICES,
    })


def student_delete(request, pk):
    """Delete a student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.get_full_name()
        student.user.delete()
        messages.success(request, f'Student {name} removed.')
        return redirect('student_list')
    return render(request, 'student/student_confirm_delete.html', {
        'student': student,
        'page_title': 'Remove Student',
    })