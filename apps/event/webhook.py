from django.dispatch import receiver
from djstripe.signals import webhook_post_validate
from djstripe.models import Session

# Signal handler to create an entry in the OtherModel when a Djstripe session event is received
@receiver(webhook_post_validate)
def create_other_model_entry(sender, event, **kwargs):
    print("Runthis function =================>")

# Connect the signal handler to the webhook_received signal
webhook_post_validate.connect(create_other_model_entry, sender=None)