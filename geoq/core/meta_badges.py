import badges
from core.models import AOI

class AOICompleter(badges.MetaBadge):
    id = "AOICompleter"
    model = AOI
    one_time_only = False
    title = "AOI Completer"
    level = "1"
    def check_aoi(self,instance):
        if instance.analyst and instance.status == "Completed":
            newscore = AOI.objects.filter(analyst=instance.analyst,status="Completed").count() * 5 + 1
            instance.analyst.get_profile().score = newscore
            instance.analyst.get_profile().save()

            # TODO: not really using score at the moment, just giving the badge to them
            # do a check against badgesettings to see if they've really earned this

            return True
        return False
    def get_user(self,instance):
        return instance.analyst


class MultiJobCompleter(badges.MetaBadge):
    id = "MultiJobCompleter"
    model = AOI
    one_time_only = False
    title = "MultiJobCompleter"
    level = "2"

    def check_aoi(self, instance):
        if instance.analyst and instance.status == "Completed":
            # Score will get updated above
            jobs = set([aoi.job for aoi in AOI.objects.filter(analyst=instance.analyst,status="Completed")])
            return len(jobs) > 1
        return False
    def get_user(self,instance):
        return instance.analyst
