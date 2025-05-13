from django.db import models

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, null=False, primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.user_id})"
