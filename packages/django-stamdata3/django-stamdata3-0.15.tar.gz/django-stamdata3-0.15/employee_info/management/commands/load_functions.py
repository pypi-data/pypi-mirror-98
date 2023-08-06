from django.core.management.base import BaseCommand

from employee_info.load_data import load_functions


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_functions()
