from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import ContactMessage,RateLimit
class Command(BaseCommand):
    help='Supprime les messages de plus de 365 jours hors échanges en cours.'
    def handle(self,*args,**options):
        now=timezone.now()
        n,_=ContactMessage.objects.filter(keep=False,created_at__lt=now-timedelta(days=365)).delete()
        RateLimit.objects.filter(expires_at__lt=now).delete()
        self.stdout.write(f'{n} ancien(s) message(s) supprimé(s).')
