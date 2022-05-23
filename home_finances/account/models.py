from django.conf import settings
from django.db import models
from django.utils.timezone import now


class OperationCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Operation(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField(default=now)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(OperationCategory, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("title", "date", "amount", "category", "user")
