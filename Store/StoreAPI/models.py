from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Box(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return f"Box {self.id}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="total_boxes_added_in_a_week",
                check=models.Q(
                    created_at__gte=timezone.now() - timezone.timedelta(days=7)  # Calculate one week ago
                )
            )
        ]

    created_at = models.DateTimeField(auto_now_add=True)  # Use auto_now_add to track creation date
