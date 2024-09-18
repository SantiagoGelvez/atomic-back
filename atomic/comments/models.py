import os
import uuid

from django.db import models

from revisions.models import Revision
from users.models import User


def upload_to_unique(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('comments/', unique_filename)


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    text = models.TextField(null=True, blank=True)
    image_s3_key = models.FileField(upload_to='comments/', null=True, blank=True)
    audio_s3_key = models.FileField(upload_to=upload_to_unique, null=True, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text[:50]}... by {self.user} on {self.revision}'
