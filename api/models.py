from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=244, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
