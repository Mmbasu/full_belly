from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from donor.models import PerishableDonation


@receiver(post_save, sender=PerishableDonation)
def delete_perishable_donation(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.pk
        instance_date = instance.created_at
        expiry_date = instance_date + timezone.timedelta(hours=24)
        time_difference = expiry_date - timezone.now()

        # Schedule deletion after 24 hours
        delete_perishable_donation_after_expiry.apply_async(args=[instance_id],
                                                            countdown=time_difference.total_seconds())


@shared_task
def delete_perishable_donation_after_expiry(instance_id):
    try:
        perishable_donation = PerishableDonation.objects.get(pk=instance_id)
        perishable_donation.delete()
    except PerishableDonation.DoesNotExist:
        pass