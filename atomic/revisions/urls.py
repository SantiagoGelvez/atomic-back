from django.urls import path

from .views import RevisionsView, RevisionCommentsView

urlpatterns = [
    path('', RevisionsView.as_view(), name='revisions'),
    path('<uuid:uuid>', RevisionsView.as_view(), name='revision'),
    path('<uuid:uuid>/comments', RevisionCommentsView.as_view(), name='revision_comments'),
]
