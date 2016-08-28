from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class UserProfile(AbstractUser):
    main = models.ForeignKey("Character", null=True, blank=True)

class Character(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=50)
    realm = models.CharField(max_length=50)
    ilvl = models.IntegerField()
    tradeskill1 = models.CharField(max_length=50, null=True, blank=True)
    tradeskill2 = models.CharField(max_length=50, null=True, blank=True)
    wowclass = models.CharField(max_length=50)
    portrait = models.CharField(max_length=2000)

    def __str__(self):
        return "{} of {}, ilvl {}".format(
            self.name,
            self.realm,
            self.ilvl,
        )

class Raid(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=2000)
    tier = models.IntegerField(unique=True)

    def __str__(self):
        return "{}, Tier {}".format(
            self.name,
            self.tier,
        )

class Boss(models.Model):
    raid = models.ForeignKey(Raid)
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=2000)
    is_dead = models.BooleanField(default=False)
    guide = models.CharField(max_length=2000, null=True, blank=True)
    ordering = models.IntegerField()

    def __str__(self):
        return "{}: {}".format(
            self.raid.name,
            self.name,
        )

class Article(models.Model):
    article_type = models.CharField(max_length=50)
    author = models.ForeignKey(UserProfile)
    tags = models.CharField(max_length=50, null=True, blank=True)
    boss = models.ForeignKey(Boss, null=True, blank=True)
    character = models.ForeignKey(Character, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=2083, null=True, blank=True)

    def __str__(self):
        return "[{}] ({}) {}...".format(
            self.article_type,
            self.author,
            self.text[:15],
        )


# Create user tokens
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
