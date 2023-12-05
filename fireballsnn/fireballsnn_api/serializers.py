from rest_framework import serializers

from . import models


class CourtNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourtName
        fields = '__all__'


class NonFormattedCourtNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NonFormattedCourtName
        fields = ('value, formatted')