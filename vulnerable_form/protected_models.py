import bleach  # sanitizes HTML contents
from django.db import models
from django.contrib.auth.models import User


class XSSProtectedComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment {self.id}"

    def clean_content(self):
        """clean and sanitize content before saving"""
        # configure bleach with allowed tags and attributes
        allowed_tags = ["p", "b", "i", "u", "em", "strong"]
        allowed_attributes = {}

        # clean the content
        cleaned_content = bleach.clean(
            self.content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True,
        )
        return cleaned_content

    def save(self, *args, **kwargs):
        self.content = self.clean_content()
        super().save(*args, **kwargs)
