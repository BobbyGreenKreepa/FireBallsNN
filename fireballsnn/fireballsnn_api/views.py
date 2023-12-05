from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from fireballsnn_api import serializers
from fireballsnn_api import models
from nuro_link_algo import neuro_link


# Create your views here.

@api_view(['POST'])
def get_cased_court_name(request):
    try:
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = serializers.CourtNameSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            court_name = tutorial_serializer.validated_data["value"]
            formatted = serializers.CourtNameSerializer(data={"value": neuro_link.solveStr(court_name)})
            tutorial_serializer.save()
            if (formatted.is_valid()):
                return JsonResponse(formatted.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(formatted.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        print("error", error)