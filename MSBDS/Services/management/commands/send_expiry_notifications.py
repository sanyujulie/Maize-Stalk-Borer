

from django.core.management.base import BaseCommand
from Services.tasks import send_expiry_reminder_notification

class Command(BaseCommand):
    help = 'Sends expiry reminder notifications to users'

    def handle(self, *args, **options):
        send_expiry_reminder_notification.delay()
        self.stdout.write(self.style.SUCCESS('Successfully sent expiry reminder notification.'))
