from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        for fixture in ('initial_steepcat', 'initial_doc_types',
                        'initial_impact_types', 'initial_time'):
            call_command('loaddata', fixture)
