from django.urls import path

from website import views

urlpatterns = [
    path("", views.index, name="index"),
    path("goals-summary", views.goals_summary, name="goals-summary"),
]
