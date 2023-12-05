from django.urls import path

from . import views

urlpatterns = [
    path("getCasedCourtName", views.get_cased_court_name)
]