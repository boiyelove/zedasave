from django.core.management import BaseCommand

class Command(BaseCommand):
	help = "Updates subscription list"

	def handler(self, *args, **kwargs):
		self.stdout.write("Subscription list update handler")