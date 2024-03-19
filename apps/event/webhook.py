from django.dispatch import receiver
from djstripe.signals import webhook_post_validate
from djstripe.models import WebhookEventTrigger
import json
from djstripe.models import Session
from apps.user.models import Event as User_event_modal


# Signal handler to create an entry in the OtherModel when a Djstripe session event is received
@receiver(webhook_post_validate)
def create_other_model_entry(sender, **kwargs):
    try:
        event_data = kwargs['instance']
        Webhook_event_data = WebhookEventTrigger.objects.filter(id = event_data.id).values("body").first()
        Webhook_event_data = json.loads(Webhook_event_data['body'])
        Webhook_event = Webhook_event_data['type'] 
        print("Webhook event -------------->", Webhook_event)
        print("Event id ------------------->", event_data.id)

        if Webhook_event == "checkout.session.completed":
            metadata_information = Webhook_event_data['data']['object']['metadata']

            # Event id 
            event_id = metadata_information['event_id']
            event_user = json.loads(metadata_information['event_user']) 


            print("Event user ----->")
            print(event_user)

            User_event_modal.objects.filter(user_id__in = event_user, event_id = event_id).update(transaction_status = "Complete", payment_id = event_data.id)


    except Exception as e:
        print(e)
