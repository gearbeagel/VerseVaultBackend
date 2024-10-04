from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_auth.choices import *
from works.models import Work


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=USER_TYPE_READER,
    )
    location = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=100, default='fa-user')

    @property
    def is_writer(self):
        return self.user_type == USER_TYPE_WRITER

    @property
    def is_reader(self):
        return self.user_type == USER_TYPE_READER


class ReaderStats(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='reader_stats')
    works_read = models.PositiveIntegerField(default=0)
    work_lists = models.PositiveIntegerField(default=0)


class WriterStats(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='writer_stats')
    works_written = models.PositiveIntegerField(default=0)

    def count_works(self):
        print("Function called!")
        return Work.objects.filter(author=self.profile.user).count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        ReaderStats.objects.create(profile=profile)
        WriterStats.objects.create(profile=profile)


@receiver(post_save, sender=Profile)
def manage_user_stats(sender, instance, **kwargs):
    if instance.is_writer:
        WriterStats.objects.get_or_create(profile=instance)
        ReaderStats.objects.get_or_create(profile=instance)
    elif instance.is_reader:
        ReaderStats.objects.get_or_create(profile=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Favorite(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='favorites')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{str(self.profile)} liked {self.work}'
