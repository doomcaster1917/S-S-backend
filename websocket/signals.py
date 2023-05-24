# from django.dispatch import receiver
# from .models import Event
# from django.db.models.signals import post_save
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
#
#
# @receiver(post_save, sender=Event)
# def broadcast_event_to_groups(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     group_id = str(instance.group.group_id)
#     event_message = str(instance)
#     async_to_sync(channel_layer.group_send)(group_id,
#         {
#             "type": "event_message",
#             "message": event_message,
#             "status": instance.type,
#             "user": str(instance.user)
#         }
#
#         )
