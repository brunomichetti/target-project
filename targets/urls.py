from django.conf.urls import url

from targets.views import TargetView

urlpatterns = [    
    url(r'', TargetView.as_view()),
]
