from django.core.management.base import BaseCommand
from substitution.off_api import OffApiData


class Command(BaseCommand):
    help = "Erase all data from the database's tables except the user table"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        data = OffApiData()
        data.get_info()
        self.stdout.write(self.style.SUCCESS(
            ' Database successfully populated '))
