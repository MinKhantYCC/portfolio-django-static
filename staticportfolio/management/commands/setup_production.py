from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Run production database setup: migrations and env-based superadmin."

    def handle(self, *args, **options):
        self.stdout.write("Running migrations...")
        call_command("migrate", interactive=False, verbosity=options.get("verbosity", 1))

        self.stdout.write("Ensuring superadmin...")
        call_command("ensure_admin", verbosity=options.get("verbosity", 1))

        self.stdout.write(self.style.SUCCESS("Production setup complete."))
