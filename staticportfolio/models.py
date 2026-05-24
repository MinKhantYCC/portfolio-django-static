from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class OrderedActiveModel(models.Model):
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["display_order", "id"]


class Profile(models.Model):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    avatar_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=160, blank=True)
    about = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    medium_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True)
    map_embed_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "id"]

    def __str__(self):
        return self.name


class Service(OrderedActiveModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Client(OrderedActiveModel):
    name = models.CharField(max_length=120)
    logo_url = models.URLField()
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Education(OrderedActiveModel):
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=180, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta(OrderedActiveModel.Meta):
        verbose_name_plural = "education"

    def __str__(self):
        return self.institution


class WorkExperience(OrderedActiveModel):
    role = models.CharField(max_length=160)
    company = models.CharField(max_length=160)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"


class Skill(OrderedActiveModel):
    name = models.CharField(max_length=120)
    proficiency = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "project categories"

    def __str__(self):
        return self.name


class Project(OrderedActiveModel):
    title = models.CharField(max_length=160)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        related_name="projects",
    )
    image_url = models.URLField(blank=True)
    project_url = models.URLField(blank=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title


class BlogPost(OrderedActiveModel):
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=120, blank=True)
    published_on = models.DateField(null=True, blank=True)
    published_label = models.CharField(max_length=40, blank=True)
    image_url = models.URLField(blank=True)
    external_url = models.URLField(blank=True)
    excerpt = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
