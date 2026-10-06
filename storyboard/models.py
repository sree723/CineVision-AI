from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Scene(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="scenes"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class ShotPrompt(models.Model):
    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name="prompts"
    )

    prompt_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt_text[:50]
class Generation(models.Model):

    IMAGE = "image"
    VIDEO = "video"

    OUTPUT_TYPES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    ]

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    ]

    prompt = models.ForeignKey(
        ShotPrompt,
        on_delete=models.CASCADE,
        related_name="generations"
    )

    output_type = models.CharField(
        max_length=10,
        choices=OUTPUT_TYPES,
        default=IMAGE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    output_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.output_type} - {self.status}"