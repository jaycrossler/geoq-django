import badges
from core.models import AOI

class AOICompleter(badges.MetaBadge):
    id = "AOICompleter"
    model = AOI
    one_time_only = True
    title = "AOI Completer"
    level = "1"
    def check_aoi(self,instance):
        if instance.analyst and instance.status == "Completed":
            import pdb
            pdb.set_trace()
            newscore = AOI.objects.filter(analyst=instance.analyst,status="Completed").count() * 5 + 1
            #TODO: check if this changed?
            instance.analyst.get_profile().score = newscore
            instance.analyst.get_profile().save()
            return True
        return False
    def get_user(self,instance):
        return instance.analyst


class MultiJobCompleter(badges.MetaBadge):
    id = "multijobcompleter"
    model = AOI
    one_time_only = True
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
