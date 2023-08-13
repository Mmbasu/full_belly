from django.core.management.base import BaseCommand
from django.utils import timezone

from donor.models import Donation


class Command(BaseCommand):
    help = 'Deletes unscheduled donations older than 24 hours.'

    def handle(self, *args, **kwargs):
        twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)
        Donation.objects.filter(
            date_posted__lt=twenty_four_hours_ago,
            is_scheduled=False
        ).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted old unscheduled donations.'))
