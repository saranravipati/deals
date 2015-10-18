import time
from datetime import datetime, date
from decimal import Decimal

from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils import timezone

# Create your models here.
class Deals(models.Model):
    mobile         = models.CharField(max_length=200)
    brand          = models.CharField(max_length=200)
    description    = models.TextField()
    price          = models.DecimalField(decimal_places=2, max_digits=8)
    status_choices = ((0, 'Active'),
                      (1, 'In Auction'),
                      (2, 'Closed'),
                      (3, 'Deleted'),
                     )
    status         = models.IntegerField(default=0, blank=True, choices=status_choices)
    won_bid        = models.ForeignKey('Bid', null=True, blank=True)
    dt_added       = models.DateTimeField(default=timezone.now, blank=True)

    def __unicode__(self):
        return "Mobile: %s -- Brand: %s -- Price: %s" % (self.mobile, self.brand, self.price)

class Bid(models.Model):
    deal     = models.ForeignKey(Deals)
    user     = models.ForeignKey(User)
    price    = models.DecimalField(decimal_places=2, max_digits=8)
    dt_added = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        unique_together = [('deal', 'user', 'price')]

    def __unicode__(self):
        return "Deal: %s -- User: %s -- Price: %s -- Date: %s" % (self.deal.id, self.user.id, self.price, self.dt_added)

