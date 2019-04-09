from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

# import models from django-friendship library
from friendship.models import Follow
from . import signals

class FollowRequest(models.Model):
    """ Model to represent follow request"""
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name="follow_requests_sent")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name="follow_requests_recieved")

    message = models.TextField(_('Message'), blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Follow Request')
        verbose_name_plural = _('Follow Requests')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "%s" % self.from_user_id

    def accept(self):
        """ Accept this follow request """
        follower = self.from_user
        followee = self.to_user
        relation = Follow.objects.add_follower(follower, followee)

        signals.follow_request_accepted.send(sender=self, from_user=follower,
                                     to_user=followee)
        self.delete() # request no longer needed

    def reject(self):
        """ reject this follow request """
        self.rejected = timezone.now()
        self.save()
        signals.follow_request_rejected.send(sender=self)

    def cancel(self):
        """ cancel this follow request """
        self.delete()
        signals.follow_request_canceled.send(sender=self)
