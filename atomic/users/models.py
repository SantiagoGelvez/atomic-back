import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from companies.models import Company


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('designer', 'Designer')
    ]
    uuid = models.UUIDField(primary_key=True, null=False, editable=False, default=uuid.uuid4)
    user_type = models.CharField(max_length=8, choices=USER_TYPE_CHOICES, default='client')
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.user_type}'
