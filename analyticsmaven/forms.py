from .models import *
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = (
            "email", "first_name", "last_name",
            "area", "industry", "tools_and_language", "experience_level", "professional_title", "overview", "language_known", "country", "timezone", "week_availability", "postal_code", "city", "phone_no", "hourly_rate", "analytics_rate",  "paid_rate"
        )
        exclude = [
            'user', 'avatar'
        ]


class EducationForm(forms.ModelForm):
    grade = forms.CharField(required=False)
    activities_socities = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = EducationDetails
        fields = "__all__"


class EmploymentForm(forms.ModelForm):
    to_month = forms.CharField(required=False)
    to_year = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = Employment
        fields = ["seeker", "title", "company", "location",
                  "from_year", "from_month", "to_month", "to_year", "currently", "description"]


class EmploymentAdminForm(forms.ModelForm):
    to_month = forms.CharField(required=False)
    to_year = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def clean_currently(self):
        currently = self.cleaned_data.get('currently')
        to_month = self.cleaned_data.get('to_month')
        to_year = self.cleaned_data.get('to_year')
        if not currently and not to_month and not to_year  :
            raise ValidationError("To month and To year is required.")
        return currently

    class Meta:
        model = Employment
        fields = ["seeker", "title", "company", "location",
                  "from_year", "from_month", "to_month", "to_year", "currently", "description"]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["company_name", 'email', "industry",
                  'language', 'tools_and_language', "contact_number", "country", ]
        exclude = ['user', 'first_name', 'last_name']


class RegistrationForm(forms.ModelForm):
    user_type = forms.CharField(required=True)
    email = forms.CharField(
        required=True,
        error_messages={
            'invalid': 'Please enter correct email',
            'required': 'Please choose email'
        })

    class Meta:
        model = MyUser
        fields = ('user_type', 'email')


class RegistrationDetailForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(password) < 8 or None:
            raise forms.ValidationError("Password must be at least 8 characters.")
        elif len(password) > 15:
            raise forms.ValidationError("Password must be not more than 15 characters.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Your Confirm passwords do not match')
        return confirm_password

    class Meta:
        model = JobSeeker
        fields = ('first_name', 'last_name')


class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(password) < 8 or None:
            raise forms.ValidationError("Password must be at least 8 characters.")
        elif len(password) > 15:
            raise forms.ValidationError("Password must be not more than 15 characters.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Your Confirm passwords do not match')
        return confirm_password

    class Meta:

        model = MyUser
        fields = ('password',)


class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(required=True,strip=False,error_messages={"required": "Please Enter Old Password"})
    new_password = forms.RegexField(regex=r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$', required=True, strip=False, error_messages={
        "invalid": "Minimum of 8 character and a maximum of 16. Must have at least three of following:uppercase letter lowercase letter, number(0-9)and/or special character/symbol.Password is case-sensitive.",
        "required": "Please Enter New Password."})
    confirm_password = forms.CharField(
        required=True,
        strip=False,
        error_messages={
            "required": "Please Enter Confirm Password"
        })

    def clean_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(new_password) < 8 or None:
            raise forms.ValidationError("Password must be at least 8 characters.")
        elif len(new_password) > 15:
            raise forms.ValidationError("Password must be not more than 15 characters.")
        return new_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError('Your Confirm passwords do not match')
        return confirm_password


class EditProfileForm(forms.ModelForm):
    country = forms.CharField()

    class Meta:
        model = JobSeeker
        fields = ('country',)


class CompanyRegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if len(password) < 8 or None:
            raise forms.ValidationError("Password must be at least 8 characters.")
        elif len(password) > 15:
            raise forms.ValidationError(
                "Password must be not more than 15 characters."
            )
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Your Confirm passwords do not match')
        return confirm_password

    class Meta:
        model = MyUser
        fields = ('first_name',)

class CompanyRegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)


    class Meta:
        model = MyUser
        fields = ('first_name',)


class JobPostStep1Form(forms.ModelForm):

    class Meta:
        model = JobManagement
        fields = ('job_name', 'description', 'company_name')


class JobPostStep2Form(forms.ModelForm):

    class Meta:
        model = JobManagement
        fields = ('number_of_employees',)


class JobPostStep3Form(forms.ModelForm):

    class Meta:
        model = JobManagement
        fields = ('type_of_project',)


class JobPostStep4Form(forms.ModelForm):

    class Meta:
        model = JobManagement
        fields = ('payment', 'duration', 'credit')


class SetLocationForm(forms.ModelForm):

    class Meta:
        model = JobSeeker
        fields = (
            'week_availability', 'country', 'timezone',
            'postal_code', 'city', 'phone_no'
        )


class SetHourlyRateForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ('analytics_rate', 'hourly_rate',
                  'paid_rate')


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        exclude = ("profession",)


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = AppliedJobs
        fields = ('user', 'job', 'reason', 'resume')






class CareerAdminModelForm(forms.ModelForm):

    def clean(self):
        resume = self.cleaned_data.get('resume', False)
        try:
            file_extenison = (resume._name).rsplit(".")
            print("File Exentension",file_extenison)
            if resume and("pdf" == file_extenison[-1] or 'docx' == file_extenison[-1] or 'doc' ==  file_extenison[-1]):
                pass
            else:
                raise ValidationError("Uploaded fle should have .pdf/.docx/.doc  type.")
        except:
            pass


    class Meta:
        model = Career
        fields = '__all__'



class BoardMemberAdminModelForm(forms.ModelForm):

    def clean(self):
        avatar = self.cleaned_data.get('avatar', False)
        try:
            file_extenison = (avatar._name).rsplit(".")
            if avatar and("jpg" == file_extenison[-1] or 'jpeg' == file_extenison[-1] or 'png' ==  file_extenison[-1] or 'gif' ==  file_extenison[-1]):
                pass
            else:
                raise ValidationError("Uploaded fle should have .jpg/.jpeg/.png/.gif type.")
        except:
            pass

    class Meta:
        model = BoardMember
        fields = '__all__'
