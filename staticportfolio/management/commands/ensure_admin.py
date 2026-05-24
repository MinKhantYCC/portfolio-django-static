import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update a Django superadmin from ADMIN_USERNAME and ADMIN_PASSWORD."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not password:
            raise CommandError("ADMIN_USERNAME and ADMIN_PASSWORD are required.")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )

        changed_fields = []
        if created:
            user.set_password(password)
            changed_fields.extend(["password", "is_staff", "is_superuser"])
        else:
            if not user.is_staff:
                user.is_staff = True
                changed_fields.append("is_staff")
            if not user.is_superuser:
                user.is_superuser = True
                changed_fields.append("is_superuser")

        if changed_fields:
            user.save(update_fields=changed_fields)

        action = "Created" if created else "Ensured"
        self.stdout.write(self.style.SUCCESS(f"{action} superadmin '{username}'."))
