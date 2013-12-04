from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

from django.db.models.signals import pre_save, post_save

class Organization(models.Model):
    name = models.CharField(max_length=250)
    primary_contact = models.ForeignKey(User) #help="If there is a problem, this is the lead for handling it.")

    class Meta:
        unique_together = ('name', 'primary_contact')

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    organization = models.ForeignKey(Organization, null=True)
    # TODO: Add authorized field --- boolean? -- this works with Staff on user model.

    """ from http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django; this is one mechanism for adding extra details (currently score for badges) to the User model """
    defaultScore = 1
    user = models.OneToOneField(User)
    score = models.IntegerField(default=defaultScore)

    def __str__(self):
          return "%s's profile" % self.user

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        user = self.user
        group_ids = [g.id for g in user.groups.all()]

        if user.is_staff and 1 not in group_ids:
            # give them default auth permissions.
            user.groups.add(1)
        elif not user.is_staff and 1 in group_ids:
            # if they are not staff and they have the permission, remove it.
            user.groups.remove(1)