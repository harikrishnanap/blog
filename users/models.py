from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='first', blank=False)
    first_name = models.CharField(max_length=100, default='first', blank=False)
    last_name = models.CharField(max_length=100, default='last', blank=False)
    image = models.ImageField(upload_to='profile_pic', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    #extra
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     # Resize image if it's too large
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)