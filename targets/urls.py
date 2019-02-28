from django.urls import path

from targets.views import TargetView, TargetMatchView, TargetDetailView

urlpatterns = [
    path('', TargetView.as_view()),
    path('matches/', TargetMatchView.as_view()),
    path('<int:pk>/', TargetDetailView.as_view()),
]
