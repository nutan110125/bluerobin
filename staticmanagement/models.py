from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from djrichtextfield.models import RichTextField
from analyticsmaven.models import MyUser

class AboutUs(models.Model):
    title = models.CharField(
        "Analytics Maven Title", max_length=200
    )
    title_description = models.TextField(
        "Title Description"
    )
    overview = models.CharField(
        "Analytics Maven Overview", max_length=200,
    )
    overview_description = RichTextField(
        "Description"
    )
    mission = models.CharField(
        "Mission and Vision", max_length=200
    )
    mission_description = RichTextField(
        "Description"
    )
    avatar = CloudinaryField(
        "About Us Banner", blank=True, null=True
    )
    avatar_2 = CloudinaryField(
        "About Us", blank=True, null=True
    )
    banner_heading = models.CharField(
        "Banner Heading", max_length=200
    )
    banner_content = models.CharField(
        "Banner Content", max_length=500
    )

    def __str__(self):
        return self.overview

    class Meta:
        verbose_name_plural = "About Us"


class Tags(models.Model):

    name = models.CharField(
        "Tags", max_length=100
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "FAQ Tags"


class FAQ(models.Model):
    tagging = models.ManyToManyField(
        Tags, related_name='tagging'
    )
    question = models.CharField(
        "Question", max_length=255, blank=True, null=True)
    answer = models.CharField("Answer", max_length=255, blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQ"


class TermsAndConditions(models.Model):
    banner = CloudinaryField(
        "Banner", blank=True, null=True
    )
    banner_heading = models.CharField(
        "Banner Heading", max_length=200
    )
    banner_content = models.CharField(
        "Banner Content", max_length=500
    )
    content = RichTextField(
        "Content"
    )

    def __str__(self):
        return "Terms & Conditions"

    class Meta:
        verbose_name_plural = "Terms and Conditions"


class HowitWorks(models.Model):
    icon = CloudinaryField("Icon",blank=False,)
    title = models.CharField(max_length=20)
    content = RichTextField(
        "Content"
    )
    def __str__(self):
        return self.content

    class Meta:
        ordering = ("-id",)
        verbose_name = "How it Works?"
        verbose_name_plural = "How it Works?"


class PrivacyPolicy(models.Model):
    banner = CloudinaryField(
        "Banner", blank=True, null=True
    )
    banner_heading = models.CharField(
        "Banner Heading", max_length=200
    )
    banner_content = models.CharField(
        "Banner Content", max_length=500
    )
    content = RichTextField(
        "Content"
    )

    def __str__(self):
        return "Privacy Policy"

    class Meta:
        verbose_name_plural = "Privacy Policy"



class ReferFriend(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE, related_name='refered')
    email = models.EmailField(max_length=50,)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Refered Friend"



class WhoAreWe(models.Model):
    title = models.CharField(max_length=20)
    content = RichTextField(
        "Content"
    )
    def __str__(self):
        return "Who we are!!!"

    class Meta:
        verbose_name_plural = "Who we are"
