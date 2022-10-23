from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import createsuperuser
from account.models import UserAccount

class Command(BaseCommand):
    help = "Create a admin user: python manage.py createadmin --username --email --password"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            dest="username",
            default=None,

            help="Specifies the username for the admin.",
        )
        parser.add_argument(
            "--email",
            dest="email",
            default=None,

            help="Specifies the email for the admin.",
        )
        parser.add_argument(
            "--password",
            dest="password",
            default=None,

            help="Specifies the password for the admin.",
        )



    def handle(self, *args, **options):
        password = options.get("password")
        username = options.get("username")
        email = options.get("email")


        if not email:
            raise CommandError("--email is required if specifying --email (format: {7:int}@student.birzeit.edu)")

        if not password:
            raise CommandError("--password is required if specifying --password")

        if not username:
            raise CommandError("--username is required if specifying --username")


        user = UserAccount(username=username, email=email)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save()
