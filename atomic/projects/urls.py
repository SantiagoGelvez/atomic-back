from django.urls import path

from .views import ProjectsView

urlpatterns = [
    path('', ProjectsView.as_view(), name='projects'),
    path('<uuid:uuid>', ProjectsView.as_view(), name='project'),
]
