from django.contrib import admin

from .models import (
    BlogPost,
    Client,
    ContactMessage,
    Education,
    Profile,
    Project,
    ProjectCategory,
    Service,
    Skill,
    Testimonial,
    WorkExperience,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "title", "email", "location")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "website_url", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "website_url")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "recommendation_message")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "institution",
        "degree",
        "start_date",
        "end_date",
        "is_current",
        "display_order",
        "is_active",
    )
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active", "is_current")
    search_fields = ("institution", "degree", "description")


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "role",
        "company",
        "start_date",
        "end_date",
        "is_current",
        "display_order",
        "is_active",
    )
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active", "is_current")
    search_fields = ("role", "company", "description")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "proficiency", "display_order", "is_active")
    list_editable = ("proficiency", "display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title", "summary")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "published_on",
        "display_order",
        "is_active",
    )
    list_editable = ("display_order", "is_active")
    list_filter = ("is_active", "category", "published_on")
    search_fields = ("title", "category", "excerpt")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("full_name", "email", "message")
    readonly_fields = ("created_at",)
