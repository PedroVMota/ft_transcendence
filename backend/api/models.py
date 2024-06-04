from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import AbstractUser

DEFAULT_IMAGE = 'api/defaultAssets/ProfilePicture.png'

def upload_to(instance, filename):
    print('instance', instance)
    return 'images/{filename}'.format(filename=filename)



    
GAMESTATUS = (
    ('W', 'Win'),
    ('L', 'Lose'),
    ('D', 'Draw'),
)

class MyUser(AbstractUser):
    profile_image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    
    def jsonInformation(self):
        return {
            'username': self.username,
            'email': self.email,
            'profile_image': self.profile_image.url if self.profile_image else None,
            'about_me': self.about_me,
            'create_date': self.create_date,
            'update_date': self.update_date
        }
        
    def UploadDefaultImage(self):
        self.profile_image = DEFAULT_IMAGE
        self.save()
    def save(self, *args, **kwargs):
        if not self.profile_image:
            self.UploadDefaultImage()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username

class PongGameHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=GAMESTATUS)
    PlayerScore = models.IntegerField()
    EnemyScore = models.IntegerField()
    def __str__(self):
        return self.user.username
    



    
    