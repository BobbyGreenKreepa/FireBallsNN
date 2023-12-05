from django.db import models


# Create your models here.
class CourtName(models.Model):
    value = models.CharField(max_length=200, blank=False, default='')

    def __str__(self):
        return self.value


class NonFormattedCourtName(models.Model):
    value = models.CharField(max_length=200, blank=False, default='')

    formatted = models.OneToOneField(
        CourtName,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return self.value
