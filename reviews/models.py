from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    movie = models.PositiveIntegerField()
    rating = models.FloatField()
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_reviews', through='Emote')
    is_spoiler = models.BooleanField(default=False)

    @property
    def num_likes(self):
        return self.emote_users.filter(emote__emotion=1).count()
    @property
    def num_dislikes(self):
        return self.emote_users.filter(emote__emotion=0).count()
    
    created_at = models.DateTimeField(auto_now_add=True)
    def time_since_created(self):
        time_difference = timezone.now() - self.created_at
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes = remainder // 60
        if days >= 1:
            return '{}일 전'.format(days)
        elif hours >= 1:
            return '{}시간 전'.format(hours)
        elif minutes >= 1:
            return " {}분 전".format(minutes)
        else:
            return '방금 전'
        
    updated_at = models.DateTimeField(auto_now=True)


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_comments', through='Emote')

    @property
    def num_likes(self):
        return self.emote_users.filter(emote__emotion=1).count()
    @property
    def num_dislikes(self):
        return self.emote_users.filter(emote__emotion=0).count()

    created_at = models.DateTimeField(auto_now_add=True)
    def time_since_created(self):
        time_difference = timezone.now() - self.created_at
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes = remainder // 60
        if days >= 1:
            return '{}일 전'.format(days)
        elif hours >= 1:
            return '{}시간 전'.format(hours)
        elif minutes >= 1:
            return " {}분 전".format(minutes)
        else:
            return '방금 전'
        
    updated_at = models.DateTimeField(auto_now=True)


class Emote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, null=True ,on_delete=models.CASCADE)
    review_comment = models.ForeignKey(ReviewComment, null=True, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=10)