from django.contrib.gis.db import models


class AOIManager(models.GeoManager):

    def add_filters(self, **kwargs):
        """
        Returns the queryset with new filters
        """
        return super(AOIManager, self).get_query_set().filter(**kwargs)

    def unassigned(self):
        """
        Returns unassigned AOIs.
        """
        return self.add_filters(status='Unassigned')

    def assigned(self):
        """
        Returns assigned AOIs.
        """
        return self.add_filters(status='Assigned')

    def in_work(self):
        """
        Returns AOIs in work.
        """
        return self.add_filters(status='In Work')

    def submitted(self):
        """
        Returns submitted AOIs.
        """
        return self.add_filters(status='Submitted')

    def completed(self):
        """
        Returns completed AOIs.
        """
        return self.add_filters(status='Completed')
