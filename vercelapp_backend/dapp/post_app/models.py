from django.db import models
from django.core.exceptions import ValidationError


class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    year = models.PositiveIntegerField()
    description = models.TextField()

    # Image upload
    image_upload = models.ImageField(
        upload_to="media/posts/",
        blank=True,
        null=True,
        help_text="Upload an image"
    )

    # Video upload
    video_upload = models.FileField(
        upload_to="media/posts/videos/",
        blank=True,
        null=True,
        help_text="Upload a short video"
    )

    # Video URL
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Video URL"
    )

    # Project link
    link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    def clean(self):
        if not self.image_upload and not self.video_upload and not self.video_url:
            raise ValidationError(
                "Please provide either image upload, video upload, or video URL."
            )