from django.db import models
from django.utils.text import slugify

class Certificate(models.Model):
    title = models.CharField(max_length=200)  # Title for the certificate
    file = models.FileField(upload_to='certificates/')  # File for the certificate
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="certificates")  # Link to Course
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.title} - {self.course.name}"


class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True, null=True)  # Store FontAwesome class for the icon
    
    class Meta:
        db_table = 'Technologies'  # Ensure correct database table name
        verbose_name_plural = "Technologies"  # Correct plural display in the admin panel

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    technologies = models.ManyToManyField(Technology, related_name="courses")  # ManyToManyField   
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Lab(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name="labs")  # Separate from problem sets
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="labs")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Lab.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProblemSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name="problem_sets")    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="problem_sets")
    slug = models.SlugField(blank=True)

    class Meta:  
        verbose_name_plural = "Problem Sets"  # Correct plural display in the admin panel

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ProblemSet.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name="projects")    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="projects")
    slug = models.SlugField(blank=True)

    class Meta:  
        verbose_name_plural = "Projects"  # Correct plural display in the admin panel

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class FinalProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name="final_projects")  # Link to technologies
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="final_projects")  # Link to a course
    screenshot_url = models.URLField(blank=True, null=True)  # Optional screenshot URL
    video_url = models.URLField(blank=True, null=True)  # Optional video URL
    slug = models.SlugField(blank=True, unique=True)  # slug field

    class Meta:  
        verbose_name_plural = "Final Project"  # Correct plural display in the admin panel

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while FinalProject.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Submission(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    submission_link = models.URLField()    
    lab = models.ForeignKey(
        "Lab",
        on_delete=models.CASCADE,
        related_name="submissions",
        blank=True,
        null=True,  # Allow it to be optional
    )
    problem_set = models.ForeignKey(
        "ProblemSet",
        on_delete=models.CASCADE,
        related_name="submissions",
        blank=True,
        null=True,  # Allow null values
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="submissions",
        blank=True,
        null=True,  # Allow null values
    )
    final_project = models.ForeignKey(
        "FinalProject",
        on_delete=models.CASCADE,
        related_name="submissions",
        blank=True,
        null=True,  # Allow it to be optional
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure at least one field is populated
        if not any([self.lab, self.problem_set, self.project, self.final_project]):
            raise ValueError("A submission must be linked to at least one: a Lab, Problem Set, Project, or Final Project.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



