from django.contrib.auth.models import User
from django.db import models


class Leave(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField(max_length=2,
                                choices =(("SL", "Sick Leave"), ("TL", "Temporary Leave"),
                                          ("PL", "Personal Leave"), ("AW", "Adverse Weather"),
                                          ("ML","Maternity leave"),))
    day = models.CharField(max_length=2,
                           choices=(("Su", "Sunday"),("Mo", "Modnday"),("Tu", "Tuesday"),
                                    ("We", "Wednesday"),("Te", "Thursday"),))
    description = models.TextField(null=True, blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    estimated_time = models.DurationField(null=True, blank=True)
    pickFrom = models.DateTimeField(null=True, blank=True)
    pickTo = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=2, default="PE",
                              choices=(("AP", "Approve"), ("DA", "Disapprove"), ("PE", "Pending"),))
    approved_by = models.ForeignKey(User,related_name='approved_by',null=True,blank=True)

    def __str__(self):
        return str(self.user)