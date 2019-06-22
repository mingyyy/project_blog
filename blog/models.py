# from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (
                Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
            )
            qq = qs.filter(or_lookup).distinct()

        return qq


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # can't change it if we use auto_now_add
    date_posted = models.DateTimeField(default=timezone.now)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        return super(Post, self).save(*args, **kwargs)


class Event(models.Model):
    location = models.CharField(max_length=200)
    details = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

    @property
    def get_html_url(self):
        url = reverse('blog:event_edit', args=(self.id,))
        return f'<a href="{url}">{self.location}</a>'

    def event_duration(self):
        delta = self.end_time - self.start_time
        if delta.days >= 0:
            return delta.days
        else:
            return False

