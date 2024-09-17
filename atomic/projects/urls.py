from django.urls import path

from .views import ProjectsView, ProjectRevisionsView

urlpatterns = [
    path('', ProjectsView.as_view(), name='projects'),
    path('<uuid:uuid>', ProjectsView.as_view(), name='project'),
    path('<uuid:uuid>/revisions', ProjectRevisionsView.as_view(), name='project_revisions'),
]
