from django.core.management import BaseCommand

class Command(BaseCommand):
	help = "A list of all subscription commands"


	def handle(self, *args, **options):
		self.stdout.write("Subscriptions handler")