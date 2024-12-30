from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Homepage
    path('courses/', views.courses, name='courses'),  # Courses page
    path('courses/<slug:course_slug>/', views.course_content, name='course_projects'),  # Course content page
    path('courses/<slug:course_slug>/labs/<slug:lab_slug>/', views.lab_details, name='lab_details'),  # Lab detail page
    path('courses/<slug:course_slug>/problem-sets/<slug:problem_set_slug>/', views.problem_set_details, name='problem_set_details'),  # Problem Set detail page
    path('courses/<slug:course_slug>/projects/<slug:project_slug>/', views.project_details, name='project_details'),  # Project detail page
    path('courses/<slug:course_slug>/final-projects/<slug:final_project_slug>/', views.final_project_details, name='final_project_details'),  # Final Project detail page
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page

    path('level-one/', views.level_one, name='level_one'),
    path('advance-level/', views.advance_level, name='advance_level'),
    path('level-two/', views.level_two, name='level_two'),  # Add views for other levels
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
