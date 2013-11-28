from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

from django.db.models.signals import pre_save, post_save

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    #favourite_snack = models.CharField(_('favourite snack'), max_length=5)

def user_post_save(sender, instance, **kwargs):
    """
        If the user is staff and they don't have default auth permissions
        assign them.
    """

    group_ids = [g.id for g in instance.groups.all()]
    if instance.is_staff and 1 not in group_ids:
        # give them default auth permissions.
        instance.groups.add(1)
    elif not instance.is_staff and 1 in group_ids:
        # if they are not staff and they have the permission, remove it.
        instance.groups.remove(1)

post_save.connect(user_post_save, sender=User)
