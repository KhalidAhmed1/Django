from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Instructor


def instructor_list(request):
    """List all instructors."""
    instructors = Instructor.objects.select_related('user').all()
    return render(request, 'instructor/instructor_list.html', {
        'instructors': instructors,
        'page_title': 'All Instructors',
    })


def instructor_detail(request, pk):
    """Show a single instructor and their courses."""
    instructor = get_object_or_404(Instructor.objects.select_related('user'), pk=pk)
    courses = instructor.courses.filter(is_active=True)
    return render(request, 'instructor/instructor_detail.html', {
        'instructor': instructor,
        'courses': courses,
        'page_title': instructor.get_full_name(),
    })


def instructor_create(request):
    """Create a new instructor (with a new User)."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        expertise  = request.POST.get('expertise', '').strip()
        bio        = request.POST.get('bio', '').strip()
        phone      = request.POST.get('phone', '').strip()
        website    = request.POST.get('website', '').strip()

        if not (first_name and last_name and email and expertise):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'instructor/instructor_form.html', {
                'page_title': 'Add Instructor',
                'form_data': request.POST,
            })

        username = f"{first_name.lower()}.{last_name.lower()}"
        # make username unique
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
        Instructor.objects.create(
            user=user,
            expertise=expertise,
            bio=bio,
            phone=phone,
            website=website,
        )
        messages.success(request, f'Instructor {user.get_full_name()} created!')
        return redirect('instructor_list')

    return render(request, 'instructor/instructor_form.html', {
        'page_title': 'Add Instructor',
    })


def instructor_edit(request, pk):
    """Edit an existing instructor."""
    instructor = get_object_or_404(Instructor, pk=pk)

    if request.method == 'POST':
        instructor.user.first_name = request.POST.get('first_name', '').strip()
        instructor.user.last_name  = request.POST.get('last_name', '').strip()
        instructor.user.email      = request.POST.get('email', '').strip()
        instructor.expertise       = request.POST.get('expertise', '').strip()
        instructor.bio             = request.POST.get('bio', '').strip()
        instructor.phone           = request.POST.get('phone', '').strip()
        instructor.website         = request.POST.get('website', '').strip()
        instructor.user.save()
        instructor.save()
        messages.success(request, 'Instructor updated!')
        return redirect('instructor_detail', pk=pk)

    return render(request, 'instructor/instructor_form.html', {
        'instructor': instructor,
        'page_title': f'Edit {instructor.get_full_name()}',
    })


def instructor_delete(request, pk):
    """Delete an instructor."""
    instructor = get_object_or_404(Instructor, pk=pk)
    if request.method == 'POST':
        name = instructor.get_full_name()
        instructor.user.delete()   # cascades to instructor
        messages.success(request, f'Instructor {name} deleted.')
        return redirect('instructor_list')
    return render(request, 'instructor/instructor_confirm_delete.html', {
        'instructor': instructor,
        'page_title': 'Delete Instructor',
    })