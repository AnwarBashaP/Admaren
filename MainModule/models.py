import datetime
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class PostModel(models.Model):
    id = models.AutoField(primary_key= True)
    title = models.CharField(max_length=250,unique=True)
    snippets = models.CharField(max_length=250,default='')
    content = models.CharField(max_length=250,default='')
    published_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'Blog'
        ordering = ('-published_at',)

    def __str__(self):
        return self.title

    def save_model(self, request, obj, form, change):
        print(request.user)
        obj.created_by = str(request.user)
        super().save_model(request, obj, form, change)


class TagsModel(models.Model):
    Tag = models.SlugField(unique=True)
    Post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    def __repr__(self):
        return self.Tag
    def __str__(self):
        return self.Tag



# @receiver(models.signals.post_save, sender=PostModel)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         string = ("%s- %s", instance.Post.title, instance.Post.snippets)
#         old_file = TagsModel.objects.get(Post=string)
#     except TagsModel.DoesNotExist:
#         return False

