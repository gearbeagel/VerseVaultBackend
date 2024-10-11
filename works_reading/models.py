from django.contrib.auth.models import User
from django.db import models

from user_auth.models import Profile
from works_reading.choices import BOOKMARK_CHOICES
from works_writing.models import Work, Chapter


# Create your models here.

class Bookmark(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    bm_type = models.CharField(max_length=50, choices=BOOKMARK_CHOICES, default=BOOKMARK_CHOICES[0][0])
    binded_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return {self.work}
