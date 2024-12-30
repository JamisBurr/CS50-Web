from django.contrib import admin
from .models import Course, Technology, Lab, ProblemSet, Project, FinalProject, Submission, Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'description')  # Display title, linked course, and description
    list_filter = ('course',)  # Enable filtering by course
    search_fields = ('title', 'description')  # Allow search by title and description

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('technologies',)

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(ProblemSet)
class ProblemSetAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(FinalProject)
class FinalProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Keep SubmissionAdmin focused
    search_fields = ('title', 'description')
    list_filter = ('problem_set', 'lab')  # Remove final_project for clarity

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    # Display name and icon fields in the list view
    list_display = ('name', 'icon')
    # Allow searching by name
    search_fields = ('name',)
    # Enable list filter for better management
    list_filter = ('name',)
