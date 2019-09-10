from .models import *
from django.contrib import admin
from django import forms
from djrichtextfield.widgets import RichTextWidget


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = [
            'avatar','banner_heading','banner_content','title', 'title_description', 'overview', 'overview_description', 'mission', 'mission_description', 'avatar_2'
        ]


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['tagging', "question", "answer"]


class TermsAndConditionsForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = TermsAndConditions
        fields = '__all__'


class HowitWorksForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = HowitWorks
        fields = '__all__'


# class PrivacyPolicyForm(forms.ModelForm):
#     content = forms.CharField()

#     class Meta:
#         model = PrivacyPolicy
#         fields = '__all__'


# widget=RichTextWidget()
