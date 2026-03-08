from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Course
from instructor.models import Instructor
from student.models import Student


def course_list(request):
    """Homepage: list all active courses."""
    courses = Course.objects.filter(is_active=True).select_related('instructor__user').prefetch_related('students')
    category_filter = request.GET.get('category', '')
    if category_filter:
        courses = courses.filter(category=category_filter)
    return render(request, 'course/course_list.html', {
        'courses': courses,
        'page_title': 'All Courses',
        'categories': Course.CATEGORY_CHOICES,
        'selected_category': category_filter,
    })


def course_detail(request, pk):
    """Show course details, instructor, and enrolled students."""
    course = get_object_or_404(
        Course.objects.select_related('instructor__user').prefetch_related('students__user'),
        pk=pk
    )
    all_students = Student.objects.select_related('user').all()
    enrolled_ids = course.students.values_list('id', flat=True)
    return render(request, 'course/course_detail.html', {
        'course': course,
        'all_students': all_students,
        'enrolled_ids': list(enrolled_ids),
        'page_title': course.title,
    })


def course_create(request):
    """Create a new course with optional image upload."""
    if request.method == 'POST':
        title         = request.POST.get('title', '').strip()
        description   = request.POST.get('description', '').strip()
        category      = request.POST.get('category', 'other')
        level         = request.POST.get('level', 'beginner')
        duration      = request.POST.get('duration_hours', 0)
        price         = request.POST.get('price', 0)
        instructor_id = request.POST.get('instructor')
        student_ids   = request.POST.getlist('students')
        image         = request.FILES.get('image')

        if not (title and description):
            messages.error(request, 'Title and description are required.')
            return render(request, 'course/course_form.html', {
                'page_title': 'Create Course',
                'instructors': Instructor.objects.select_related('user').all(),
                'students': Student.objects.select_related('user').all(),
                'categories': Course.CATEGORY_CHOICES,
                'levels': Course.LEVEL_CHOICES,
                'form_data': request.POST,  # ← بنبعته لما يكون POST فيه error
            })

        course = Course.objects.create(
            title=title,
            description=description,
            category=category,
            level=level,
            duration_hours=int(duration) if duration else 0,
            price=float(price) if price else 0,
            instructor_id=instructor_id if instructor_id else None,
            image=image,
        )
        if student_ids:
            course.students.set(student_ids)

        messages.success(request, f'Course "{course.title}" created!')
        return redirect('course_detail', pk=course.pk)

    # GET request - بنبعت form_data فاضي عشان الـ template يلاقيه
    return render(request, 'course/course_form.html', {
        'page_title': 'Create Course',
        'instructors': Instructor.objects.select_related('user').all(),
        'students': Student.objects.select_related('user').all(),
        'categories': Course.CATEGORY_CHOICES,
        'levels': Course.LEVEL_CHOICES,
        'form_data': {},  # ← فاضي في GET
    })


def course_edit(request, pk):
    """Edit an existing course."""
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.title          = request.POST.get('title', '').strip()
        course.description    = request.POST.get('description', '').strip()
        course.category       = request.POST.get('category', 'other')
        course.level          = request.POST.get('level', 'beginner')
        course.duration_hours = int(request.POST.get('duration_hours', 0) or 0)
        course.price          = float(request.POST.get('price', 0) or 0)
        instructor_id         = request.POST.get('instructor')
        course.instructor_id  = instructor_id if instructor_id else None
        student_ids           = request.POST.getlist('students')

        if 'image' in request.FILES:
            course.image = request.FILES['image']

        course.save()
        course.students.set(student_ids)

        messages.success(request, f'Course "{course.title}" updated!')
        return redirect('course_detail', pk=pk)

    return render(request, 'course/course_form.html', {
        'course': course,
        'page_title': f'Edit: {course.title}',
        'instructors': Instructor.objects.select_related('user').all(),
        'students': Student.objects.select_related('user').all(),
        'categories': Course.CATEGORY_CHOICES,
        'levels': Course.LEVEL_CHOICES,
        'selected_students': list(course.students.values_list('id', flat=True)),
        'form_data': {},  # ← فاضي عشان الـ template يلاقيه
    })


def course_delete(request, pk):
    """Delete a course."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'Course "{title}" deleted.')
        return redirect('course_list')
    return render(request, 'course/course_confirm_delete.html', {
        'course': course,
        'page_title': 'Delete Course',
    })


def enroll_student(request, course_pk):
    """Enroll or unenroll a student from a course."""
    if request.method == 'POST':
        course     = get_object_or_404(Course, pk=course_pk)
        student_id = request.POST.get('student_id')
        action     = request.POST.get('action', 'enroll')
        student    = get_object_or_404(Student, pk=student_id)

        if action == 'enroll':
            course.students.add(student)
            messages.success(request, f'{student.get_full_name()} enrolled in {course.title}!')
        else:
            course.students.remove(student)
            messages.info(request, f'{student.get_full_name()} unenrolled from {course.title}.')

        return redirect('course_detail', pk=course_pk)
    return redirect('course_list')