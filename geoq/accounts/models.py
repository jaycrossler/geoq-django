from datetime import datetime
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

    def __str__(self):
          return self.name

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'))
    organization = models.ForeignKey(Organization, null=True)

    # Badge scores
    defaultScore = 1
    score = models.IntegerField(default=defaultScore)

    def __str__(self):
        print self
        #return "%s, %s, %s" % self.user, self.organization, self.email

class UserAuthorization(models.Model):
    user = models.ForeignKey(User)
    authorized = models.BooleanField(help_text='Check this to approve member access.')
    permissions_granted_by = models.ForeignKey(User, null=True, blank=True,
        related_name='permissions_granted_by')
    permission_granted_on = models.DateTimeField(auto_now_add=True, default=datetime.now())
    user_profile = models.ForeignKey(UserProfile)

    def __str__(self):
          return "%s's authorization info" % self.user

    def save(self, *args, **kwargs):
        user_presave = User.objects.get(pk=self.user.id)
        super(UserProfile, self).save(*args, **kwargs)
        # TODO -- make this work!
        # Grant default permissions to user if they are authorized.
        group_ids = [g.id for g in self.user.groups.all()]
        if self.authorized and 1 not in group_ids:
            # give them default auth permissions.
            self.user.groups.add(1)
            self.user.is_staff = True
            self.user.save()
        elif not self.authorized and 1 in group_ids:
            # if they are not staff and they have the permission, remove it.
            self.user.groups.remove(1)

        # TODO -- make this work!
        # *** If person is authorized and part of an organization, then they can add people from that org.
        # *** save permissions_granted_by as the user that is granting th permissions.
        # if self.authorized and not user_presave.authorized:
        #     permissions_granted_by

        #     and self.authorized != user_presave.authorized: