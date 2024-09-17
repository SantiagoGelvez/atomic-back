from django.urls import path

from .views import RevisionsView

urlpatterns = [
    path('', RevisionsView.as_view(), name='revisions'),
    path('<uuid:uuid>', RevisionsView.as_view(), name='revision'),
]
