from django.core.management.base import BaseCommand, CommandError
from utils.initial_user_groups_setup import setup


class Command(BaseCommand):
    help = 'Starts parsing documents'

    def handle(self, *args, **options):
        setup()