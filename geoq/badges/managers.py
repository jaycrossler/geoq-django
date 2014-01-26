from django.db import models
from . import registered_badges

class BadgeManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(id__in=registered_badges.keys())
        