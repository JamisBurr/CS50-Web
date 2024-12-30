from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Certificate, Lab, ProblemSet, Project, FinalProject, Submission  # Updated imports
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

# Home/Portfolio page
@cache_page(60 * 60)  # Cache for 1 hour
def index(request):
    return render(request, 'index.html')  # Ensure this points to your `home.html`

# Courses Page
@cache_page(60 * 60)
def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

# View for a specific course's content
@cache_page(60 * 60)
def course_content(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    certificates = course.certificates.all() 
    labs = course.labs.all()
    problem_sets = course.problem_sets.all()
    projects = course.projects.all()
    final_projects = course.final_projects.all()
    return render(request, 'course_content.html', {
        'course': course,
        'certificates': certificates,
        'labs': labs,
        'problem_sets': problem_sets,
        'projects': projects,
        'final_projects': final_projects,
    })

@cache_page(60 * 60)
def lab_details(request, course_slug, lab_slug):
    # Get the course and lab set
    course = get_object_or_404(Course, slug=course_slug)
    lab = get_object_or_404(Lab, slug=lab_slug, course=course)

    # Get the submissions
    submissions = lab.submissions.all()
    
    # Pass course, lab and submissions to the template
    context = {
        'course': course,
        'lab': lab,
        'submissions': submissions,
    }
    return render(request, 'lab_details.html', context)

@cache_page(60 * 60)
def problem_set_details(request, course_slug, problem_set_slug):
    # Get the course and problem set
    course = get_object_or_404(Course, slug=course_slug)
    problem_set = get_object_or_404(ProblemSet, slug=problem_set_slug, course=course)
    
    # Get the submissions
    submissions = problem_set.submissions.all()
    
    # Pass course, problem and submissions to the template
    context = {
        'course': course,
        'problem_set': problem_set,
        'submissions': submissions,
    }
    return render(request, 'problem_set_details.html', context)

@cache_page(60 * 60)
def project_details(request, course_slug, project_slug):
    # Get the course and project
    course = get_object_or_404(Course, slug=course_slug)
    project = get_object_or_404(Project, slug=project_slug, course=course)
    
    # Get the submissions
    submissions = project.submissions.all()
    
    # Pass course, project, and submissions to the template
    context = {
        'course': course,
        'project': project,
        'submissions': submissions,
    }
    return render(request, 'project_details.html', context)

@cache_page(60 * 60)
def final_project_details(request, course_slug, final_project_slug):
    # Get the course and final project
    course = get_object_or_404(Course, slug=course_slug)
    final_project = get_object_or_404(FinalProject, slug=final_project_slug, course=course)
    
    # Get the submissions
    submissions = final_project.submissions.all()
    
     # Process YouTube URL
    video_url = final_project.video_url
    if 'youtu.be' in video_url:
        video_id = video_url.split('/')[-1]
        final_project.embed_url = f'https://www.youtube.com/embed/{video_id}'
    elif 'youtube.com' in video_url:
        video_id = video_url.split('v=')[1]
        final_project.embed_url = f'https://www.youtube.com/embed/{video_id}'
    else:
        final_project.embed_url = video_url
        
    # Pass course, final project, and submissions to the template
    context = {
        'course': course,
        'final_project': final_project,
        'submissions': submissions,
    }
    return render(request, 'final_project_details.html', context)

# About Page
@cache_page(60 * 60)
def about(request):
    return render(request, 'about.html')

# Contact Page
@cache_page(60 * 60)
def contact(request):
    return render(request, 'contact.html')

def level_one(request):
    # Initialize session for level if it doesn't exist
    if 'level' not in request.session:
        request.session['level'] = 1  # Set default level
    return render(request, 'level_one.html')

def advance_level(request):
    if request.method == "POST":
        current_level = request.session.get('level', 1)
        if current_level == 1:
            request.session['level'] = 2  # Advance to Level 2
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'You are not on the right level!'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def level_two(request):
    # Check if the user has completed Level 1
    if request.session.get('level', 1) < 2:  # Default to Level 1 if no session key exists
        return redirect('level_one')  # Redirect to Level 1
    return render(request, 'level_two.html')  # Render Level 2 page