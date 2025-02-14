from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    """
           返回对象的字符串表示形式。

           该方法被调用时，会返回对象的名称属性，用于在打印或转换为字符串时显示对象的名称。

           返回:
               str: 对象的名称字符串。
           """
    def __str__(self):
        return self.name


    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    """
           获取主题中最新的帖子。

           本方法用于查询与当前主题相关的最新帖子。它通过筛选属于同一主题的帖子对象，
           并按照创建时间降序排序，最后返回排序后的第一条帖子信息。

           返回:
               最新的帖子对象，如果不存在则为None。
           """
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

# Create your models here.
