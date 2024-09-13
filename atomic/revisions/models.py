import uuid

from django.db import models

from projects.models import Project
from users.models import User


class Revision(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    attempt = models.PositiveIntegerField()
    file_extension = models.CharField(max_length=8)
    file_s3_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project_uuid} - {self.attempt}'
