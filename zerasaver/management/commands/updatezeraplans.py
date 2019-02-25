from django.core.management import BaseCommand


class Command(BaseCommand):
	help = "updates zeraplan details from paystack"


	def handle(self, *args, **options):
		self.stdout.write("Zeraplan Update Handler")