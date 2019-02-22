from django.urls import path

from targets.views import TargetView

urlpatterns = [    
    path('', TargetView.as_view()),
]
