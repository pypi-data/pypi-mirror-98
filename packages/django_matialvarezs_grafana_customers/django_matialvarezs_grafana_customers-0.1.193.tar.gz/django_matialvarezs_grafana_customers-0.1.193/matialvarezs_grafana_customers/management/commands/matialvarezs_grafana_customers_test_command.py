from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from matialvarezs_grafana_customers import utils as matialvarezs_grafana_customers_utils
import os

class Command(BaseCommand):
	
	def add_arguments(self, parser):
		pass #parser.add_argument('-f', '--foo')

	def handle(self, *args, **options):
		# foo = options["foo"]
		pass
