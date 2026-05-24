import json
from pathlib import Path

from django.contrib import messages
from django.db import DatabaseError, OperationalError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.formats import date_format

from .forms import ContactMessageForm
from .models import (
    BlogPost,
    Client,
    Education,
    Profile,
    Project,
    ProjectCategory,
    Service,
    Skill,
    WorkExperience,
)


INFO_PATH = Path(__file__).resolve().parent / "info.json"


def _load_fallback_data():
    with INFO_PATH.open(encoding="utf-8") as info_file:
        return json.load(info_file)


def _format_date(value):
    if not value:
        return ""
    return date_format(value, "N j, Y")


def _format_period(start_date, end_date, is_current):
    start = _format_date(start_date)
    end = "Present" if is_current else _format_date(end_date)
    if start and end:
        return f"{start} - {end}"
    return start or end


def _fallback_when_empty(queryset, fallback_value, serializer):
    try:
        records = list(queryset)
    except (DatabaseError, OperationalError):
        return fallback_value
    if records:
        return [serializer(record) for record in records]
    return fallback_value


def _profile_context(fallback):
    try:
        profile = Profile.objects.filter(is_active=True).first()
    except (DatabaseError, OperationalError):
        return fallback
    if not profile:
        return fallback

    birthday_display = _format_date(profile.birthday)
    return {
        "name": profile.name,
        "title": profile.title,
        "avatar_url": profile.avatar_url,
        "favicon_url": profile.favicon_url,
        "email": profile.email,
        "phone": profile.phone,
        "birthday": birthday_display,
        "birthday_iso": profile.birthday.isoformat() if profile.birthday else "",
        "location": profile.location,
        "about": profile.about,
        "github_url": profile.github_url,
        "linkedin_url": profile.linkedin_url,
        "medium_url": profile.medium_url,
        "resume_url": profile.resume_url,
        "map_embed_url": profile.map_embed_url,
    }


def _build_portfolio_context(contact_form):
    fallback = _load_fallback_data()

    project_categories = _fallback_when_empty(
        ProjectCategory.objects.filter(is_active=True),
        fallback.get("project_categories", []),
        lambda category: {"name": category.name, "slug": category.slug},
    )

    context = {
        "profile": _profile_context(fallback.get("profile", {})),
        "services": _fallback_when_empty(
            Service.objects.filter(is_active=True),
            fallback.get("services", []),
            lambda service: {
                "title": service.title,
                "description": service.description,
                "icon_url": service.icon_url,
            },
        ),
        "clients": _fallback_when_empty(
            Client.objects.filter(is_active=True),
            fallback.get("clients", []),
            lambda client: {
                "name": client.name,
                "logo_url": client.logo_url,
                "website_url": client.website_url,
            },
        ),
        "education": _fallback_when_empty(
            Education.objects.filter(is_active=True),
            fallback.get("education", []),
            lambda education: {
                "title": " ".join(
                    part for part in [education.institution, f"({education.degree})" if education.degree else ""] if part
                ),
                "period": _format_period(
                    education.start_date,
                    education.end_date,
                    education.is_current,
                ),
                "description": education.description,
            },
        ),
        "experience": _fallback_when_empty(
            WorkExperience.objects.filter(is_active=True),
            fallback.get("experience", []),
            lambda experience: {
                "role": experience.role,
                "company": experience.company,
                "period": _format_period(
                    experience.start_date,
                    experience.end_date,
                    experience.is_current,
                ),
                "description": experience.description,
            },
        ),
        "skills": _fallback_when_empty(
            Skill.objects.filter(is_active=True),
            fallback.get("skills", []),
            lambda skill: {
                "name": skill.name,
                "proficiency": skill.proficiency,
            },
        ),
        "project_categories": project_categories,
        "projects": _fallback_when_empty(
            Project.objects.filter(is_active=True).select_related("category"),
            fallback.get("projects", []),
            lambda project: {
                "title": project.title,
                "category": project.category.name,
                "category_key": project.category.name.lower(),
                "image_url": project.image_url,
                "project_url": project.project_url,
                "summary": project.summary,
            },
        ),
        "blogs": _fallback_when_empty(
            BlogPost.objects.filter(is_active=True),
            fallback.get("blogs", []),
            lambda blog: {
                "title": blog.title,
                "category": blog.category,
                "published_display": blog.published_label or _format_date(blog.published_on),
                "published_iso": blog.published_on.isoformat() if blog.published_on else "",
                "image_url": blog.image_url,
                "external_url": blog.external_url,
                "excerpt": blog.excerpt,
            },
        ),
        "contact_form": contact_form,
    }
    return context


def index(request):
    if request.method == "POST":
        contact_form = ContactMessageForm(request.POST)
        if contact_form.is_valid():
            try:
                contact_form.save()
            except (DatabaseError, OperationalError):
                messages.error(
                    request,
                    "The contact database is temporarily unavailable. Please email me directly.",
                )
            else:
                messages.success(request, "Thanks. Your message has been saved.")
                return redirect(f"{reverse('home')}#contact")
        messages.error(request, "Please correct the contact form and try again.")
    else:
        contact_form = ContactMessageForm()

    return render(
        request,
        "staticportfolio/index.html",
        _build_portfolio_context(contact_form),
    )
