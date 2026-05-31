from django.core.management import BaseCommand, CommandError, call_command
from django.db import connections


class Command(BaseCommand):
    help = "Run production database setup: migrations and env-based superadmin."

    def add_arguments(self, parser):
        parser.add_argument(
            "--allow-sqlite",
            action="store_true",
            help="Allow setup against SQLite. Intended only for local development.",
        )

    def handle(self, *args, **options):
        database = connections["default"].settings_dict
        engine = database.get("ENGINE", "")
        host = database.get("HOST") or "local file"
        name = database.get("NAME") or ""

        self.stdout.write(f"Database engine: {engine}")
        self.stdout.write(f"Database host: {host}")
        self.stdout.write(f"Database name: {name}")

        if "sqlite3" in engine and not options["allow_sqlite"]:
            raise CommandError(
                "Refusing to run production setup against SQLite. "
                "Pull/set DATABASE_URL or POSTGRES_URL for the production PostgreSQL database, "
                "or pass --allow-sqlite only for local development."
            )

        self.stdout.write("Running migrations...")
        call_command("migrate", interactive=False, verbosity=options.get("verbosity", 1))

        self.stdout.write("Ensuring superadmin...")
        call_command("ensure_admin", verbosity=options.get("verbosity", 1))

        self.stdout.write(self.style.SUCCESS("Production setup complete."))
