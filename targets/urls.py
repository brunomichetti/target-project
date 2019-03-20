from django.urls import path

from targets.views import (
    TargetView,
    TargetMatchesView,
    TargetDetailView,
    MatchMessagesDetailView
)

urlpatterns = [
    path('', TargetView.as_view()),
    path('matches/', TargetMatchesView.as_view()),
    path('<int:pk>/', TargetDetailView.as_view()),
    path('<int:t_id>/matches/<int:m_id>/', MatchMessagesDetailView.as_view()),
]
