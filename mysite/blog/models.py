from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from PIL import Image as PIL_Image

# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=100)
    content = HTMLField(verbose_name="Tekstas", max_length=8000)
    created = models.DateTimeField(verbose_name="Sukūrimo data", auto_now_add=True)
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True)


    def num_comments(self):
        return self.comments.count()

    class Meta:
        ordering = ["-created"]

class Comment(models.Model):
    content = models.TextField(verbose_name="Tekstas", max_length=1000)
    created = models.DateTimeField(verbose_name="Sukūrimo data", auto_now_add=True)
    post = models.ForeignKey(to="Post", verbose_name="Įrašas", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-created"]

class Image(models.Model):
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to="post_photos", null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL_Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)