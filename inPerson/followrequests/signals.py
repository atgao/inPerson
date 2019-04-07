from django.dispatch import Signal

follow_request_created = Signal()
follow_request_rejected = Signal()
follow_request_canceled = Signal()
follow_request_accepted = Signal(providing_args=['from_user', 'to_user'])
