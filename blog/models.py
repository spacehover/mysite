from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish_flag=True)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    #content = RichTextField()
    content = RichTextUploadingField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True,  null=True)
    publish_flag = models.BooleanField(default=False)

    objects = PostQuerySet.as_manager();

    def publish(self):
        self.published_date = timezone.now()
        self.publish_flag = True
        self.save()

    def appreoved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
