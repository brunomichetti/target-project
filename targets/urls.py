from django.urls import path

from targets.views import TargetView, TargetMatchesView, TargetDetailView

urlpatterns = [
    path('', TargetView.as_view()),
    path('matches/', TargetMatchesView.as_view()),
    path('<int:pk>/', TargetDetailView.as_view()),
]
