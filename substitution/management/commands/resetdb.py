from django.core.management.base import BaseCommand
from substitution.models import Product, Categories, Favorites
from authentification.models import User


class Command(BaseCommand):
    help = "Erase all data from the database's tables except the user table"

    def handle(self, *args, **options):
        favorite = Favorites.objects.all()
        favorite.delete()
        product = Product.objects.all()
        product.delete()
        category = Categories.objects.all()
        category.delete()
        users = User.objects.filter(id__gt=1)
        users.delete()
        self.stdout.write(self.style.SUCCESS(
            ' Successfully erased databases '))
