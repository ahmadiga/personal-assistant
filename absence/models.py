import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone




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
    pickFrom = models.CharField(max_length=200, default=timezone.now())
    pickTo = models.CharField(max_length=200, default=timezone.now())
    status = models.CharField(max_length=2, default="PE",
                              choices=(("AP", "Approve"), ("DA", "Disapprove"), ("PE", "Pending"),))
    approved_by = models.ForeignKey(User,related_name='approved_by',null=True,blank=True)

    def submit(self):
        self.submitted_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.user)