from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


from django.db.models.signals import pre_save, post_save

class Organization(models.Model):
    name = models.CharField(max_length=250)
    primary_contact = models.ForeignKey(User, help_text="Contact for org.")

    class Meta:
        unique_together = ('name', 'primary_contact')

    def __str__(self):
        return self.name

class EmailDomain(models.Model):
    email_domain = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.email_domain

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'))
    email = models.CharField(max_length=250, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True,
        help_text="If '------', no Organization records share the email domain.")

    # Badge scores
    defaultScore = 1
    score = models.IntegerField(default=defaultScore)

    def __str__(self):
        return "%s, %s, %s" % (self.user, self.organization, self.email)

    def clean(self):
        """
            Make sure that organization assigned matches the email and
            that the email matches the organization.
        """

        #TODO -- add styling to fields when error occurs.-- Right now
        # there is just an error at the top of the admin.

        # Make sure email matches email in user account
        if self.email != self.user.email:
            self.email = self.user.email

        domain = self.email.split('@')[1]
        if self.organization:
            if domain and domain not in self.organization.emaildomain_set.all():
                    raise ValidationError('User email domain must be in \
                        Organization domain options. Please add to the \
                        Organization record OR add a new Organization. Changes \
                        to this record were not saved. ')
        else:
            # If the user doesn't have an org, but they have an email
            # assign them an organization.
            try:
                email_domain = EmailDomain.objects.get(email_domain=domain)
                org = email_domain.org

                if org:
                    if self.organization != org:
                        self.organization = org

            except EmailDomain.DoesNotExist:
                raise ValidationError('There is no organization in the database \
                    with the email domain of %s. Please add one before continuing \
                    . Changes to this record were not saved.'
                    % domain)


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