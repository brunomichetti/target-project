from django.urls import path

from targets.views import TargetView, TargetMatchView

urlpatterns = [
    path('', TargetView.as_view()),
    path('matches/', TargetMatchView.as_view())
]
