from django.db import models
from utils import registered_badges

class BadgeManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(id__in=registered_badges.keys())
        