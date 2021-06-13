from django.db import models


# Create your models here.
class Stoke(models.Model):
    strikePrice = models.FloatField(null=True, blank=True, default=None)
    Option = models.CharField(max_length=50,blank=True)
    expiry_dt = models.DateField(null=True, blank=True, default=None)
    c_Oi = models.FloatField(null=True, blank=True, default=None)
    c_ChangeInOi = models.FloatField(null=True, blank=True, default=None)
    c_Volume = models.FloatField(null=True, blank=True, default=None)
    c_Iv = models.FloatField(null=True, blank=True, default=None)
    c_Ltp = models.FloatField(null=True, blank=True, default=None)
    c_Chng = models.FloatField(null=True, blank=True, default=None)
    c_BidQty = models.FloatField(null=True, blank=True, default=None)
    c_BidPrice = models.FloatField(null=True, blank=True, default=None)
    c_AskPrice = models.FloatField(null=True, blank=True, default=None)
    c_ASkQty = models.FloatField(null=True, blank=True, default=None)
    p_BidQty = models.FloatField(null=True, blank=True, default=None)
    p_BidPrice = models.FloatField(null=True, blank=True, default=None)
    p_AskPrice = models.FloatField(null=True, blank=True, default=None)
    p_AskQty = models.FloatField(null=True, blank=True, default=None)
    p_Chng = models.FloatField(null=True, blank=True, default=None)
    p_Ltp = models.FloatField(null=True, blank=True, default=None)
    p_Iv = models.FloatField(null=True, blank=True, default=None)
    p_Volume = models.FloatField(null=True, blank=True, default=None)
    p_ChangeInOi = models.FloatField(null=True, blank=True, default=None)
    p_Oi = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        ordering = ["expiry_dt","strikePrice"]