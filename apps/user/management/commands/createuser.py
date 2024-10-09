from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.db import IntegrityError

from apps.user.models import User


class Command(BaseCommand):
    help = 'Create a new user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address of the user')
        parser.add_argument('--birth_date', type=str, help='Birth date of the user (format: YYYY-MM-DD)')
        parser.add_argument('--password', type=str, help='Password for the user')
        parser.add_argument('--username', type=str, help='Optional username for the user')
        parser.add_argument('--phone', type=str, help='Optional phone number for the user')
        parser.add_argument('--full_name', type=str, help='Optional full name of the user')

    def handle(self, *args, **kwargs):
        email = kwargs['email'] or self.get_valid_email()
        birth_date = kwargs['birth_date'] or self.get_valid_birth_date()
        password = kwargs['password'] or self.get_valid_password()

        username = kwargs.get('username', '')
        phone = kwargs.get('phone', '')
        full_name = kwargs.get('full_name', '')

        try:
            user = User.objects.create_user(
                email=email,
                birth_date=birth_date,
                password=password,
                username=username,
                phone=phone,
                full_name=full_name
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.email}'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))

    def get_valid_email(self):
        while True:
            email = input('Enter email: ')
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    self.stdout.write(self.style.ERROR('This email is already in use. Please try a different email.'))
                else:
                    return email
            except ValidationError:
                self.stdout.write(self.style.ERROR('Invalid email format. Please try again.'))

    def get_valid_birth_date(self):
        while True:
            birth_date = input('Enter birth date (YYYY-MM-DD): ')
            try:
                # Validate the birth date format
                datetime.strptime(birth_date, '%Y-%m-%d')
                return birth_date
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Please use YYYY-MM-DD.'))

    def get_valid_password(self):
        while True:
            password = input('Enter password: ')
            if password:
                return password
            else:
                self.stdout.write(self.style.ERROR('Password cannot be empty.'))
