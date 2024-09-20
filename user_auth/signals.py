from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Work, WriterStats


@receiver(post_save, sender=Work)
@receiver(post_delete, sender=Work)
def update_writer_stats(sender, instance, **kwargs):
    try:
        writer_stats = instance.author.profile.writer_stats
        writer_stats.works_written = writer_stats.count_works()
        writer_stats.save()
    except WriterStats.DoesNotExist:
        pass
