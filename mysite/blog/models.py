from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=100)
    content = models.TextField(verbose_name="Tekstas", max_length=8000)
    created = models.DateTimeField(verbose_name="Sukūrimo data", auto_now_add=True)
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True)


    def num_comments(self):
        return self.comments.count()

class Comment(models.Model):
    content = models.TextField(verbose_name="Tekstas", max_length=1000)
    created = models.DateTimeField(verbose_name="Sukūrimo data", auto_now_add=True)
    post = models.ForeignKey(to="Post", verbose_name="Įrašas", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True)
