from django.contrib.auth.models import User

# Create your models here.
from django.db import models

from works.choices import LANGUAGE_CHOICES, LANGUAGE_ENGLISH


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    canonical = models.BooleanField(default=False)
    tag_type = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['canonical']),
        ]

    def __str__(self):
        return self.name


class Work(models.Model):
    title = models.CharField(max_length=255, null=False)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default=LANGUAGE_ENGLISH, help_text="Language code")
    summary = models.TextField(blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['language']),
            models.Index(fields=['posted']),
        ]

    def __str__(self):
        return self.title

    def update_word_count(self):
        total_word_count = sum(chapter.word_count for chapter in self.chapters.all())
        self.word_count = total_word_count
        self.save()


class Chapter(models.Model):
    work = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(null=True)
    position = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    word_count = models.IntegerField(blank=True, null=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['work']),
        ]

    def save(self, *args, **kwargs):
        self.word_count = len(self.content.split())
        super().save(*args, **kwargs)
        self.work.update_word_count()

    def __str__(self):
        return self.title
