import uuid
import cloudinary
from timezone_field import TimeZoneField
from cloudinary.models import CloudinaryField
from templated_email import send_templated_mail

from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from captcha.fields import ReCaptchaField


class AnalyticsRate(models.Model):
    fees = models.FloatField("Analytics Mavens Fees")

    class Meta:
        verbose_name_plural = "Analytic's Rate"


class Name(models.Model):
    name = models.CharField(
        'Name', max_length=50, unique=True, default=""
    )
    CREATEDBY = (
        ("AM", "AM"),
        ("USER", "USER"),
    )
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(
        "Created By", max_length=20, default="AM", choices=CREATEDBY
    )

    def __str__(self):
        return self.name

    class Meta:
        """Abstract class for Tools & Language,Indusrty and Area"""
        abstract = True


class Area(Name):

    class Meta:
        verbose_name_plural = "Analytic's Area"
        ordering = ('id',)


class Industry(Name):

    class Meta:
        verbose_name_plural = "Analytic's Industry"
        ordering = ('id',)


class Skills(Name):

    class Meta:
        verbose_name_plural = "Analytic's Tools & Language"
        ordering = ('id',)


class Country(Name):
    class Meta:
        verbose_name_plural = "Analytic's Countries"
        ordering = ('name',)


class Timezone(Name):
    priority = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Analytic's Timezone"
        ordering = ('priority',)


class Hours(Name):
    class Meta:
        verbose_name_plural = "Analytic's Hours"
        ordering = ('id',)


class Language(models.Model):
    language = models.CharField(
        "Language", max_length=40, blank=True, null=True)
    CREATEDBY = (
        ("AM", "AM"),
        ("USER", "USER"),
    )
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(
        "Created By", max_length=20, default="AM", choices=CREATEDBY
    )

    def __str__(self):
        return self.language

    class Meta:
        verbose_name_plural = "Analytic's Language"


class MyUserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=''):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class AbstractUser(models.Model):
    avatar = CloudinaryField(
        "User Image", blank=True, null=True
    )
    email = models.EmailField(
        "Email Address", unique=True
    )
    contact_number = models.CharField(
        "Contact Number", max_length=15
    )
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )


class MyUser(AbstractBaseUser):
    """
    Creates and saves a superuser with the given email and password
    """
    USERTYPE = (
        ("Job Seeker", "Job Seeker"),
        ("Company", "Company"),
    )

    SIGNUPTYPE = (
        ("Analytics Maven", "Analytics Maven"),
        ("linkedin-oauth2", "Linked In"),
        ("google-oauth2", "Google"),
        ("facebook-oauth2", "Facebook"),
    )
    sign_up = models.CharField(
        "SignUp Type", max_length=20, default='Analytics Maven', choices=SIGNUPTYPE
    )
    user_type = models.CharField(
        "User Type", max_length=20, default='Job Seeker', choices=USERTYPE
    )
    avatar = CloudinaryField(
        "User Image", blank=True, null=True
    )
    email = models.EmailField(
        "Email Address", unique=True
    )
    paypal_email = models.EmailField(
        "Paypal Address", blank=True, null=True
    )
    first_name = models.CharField(
        "First Name", max_length=40, blank=True, null=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, blank=True, null=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    accepting_terms = models.BooleanField(
        "Terms & Condition", default=False
    )
    is_superuser = models.BooleanField(
        "Super User", default=False
    )
    is_staff = models.BooleanField(
        "Staff", default=False
    )
    is_active = models.BooleanField(
        "Status", default=False
    )
    is_online = models.BooleanField(
        "Online", default=False
    )
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_short_name(self):
        return self.email

    def send_forgot_mail(self, message):
        try:
            send_templated_mail(
                template_name='user_management/forgot_password.email',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.email],
                context={
                    "message": message,
                    "first": self.email,
                },
            )
        except Exception as e:
            print("Exception as e", e)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"


class JobSeeker(AbstractUser):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='job_seeker'
    )
    first_name = models.CharField(
        "First Name", max_length=40, blank=True, null=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, blank=True, null=True
    )
    area = models.ManyToManyField(
        Area, related_name='job_seeker_area'
    )
    industry = models.ManyToManyField(
        Industry, related_name='job_seeker_industry'
    )
    tools_and_language = models.ManyToManyField(
        Skills, related_name='job_seeker_tools_and_language'
    )
    EXPERIENCE = (
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Expert", "Expert"),
    )
    experience_level = models.CharField(
        max_length=30, default="Beginner", choices=EXPERIENCE
    )
    professional_title = models.CharField(
        "Professional Title", max_length=500, blank=True, null=True
    )
    overview = models.TextField(
        "Overview", blank=True, null=True
    )
    language_known = models.ManyToManyField(
        Language, related_name='job_seeker_language'
    )

    week_availability = models.ForeignKey(
        Hours, on_delete=models.CASCADE, related_name='job_seeker_hours', null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='job_seeker_country', null=True, blank=True
    )
    postal_code = models.CharField(
        "Postal Code", max_length=10, blank=True, null=True
    )
    city = models.CharField(
        'City', max_length=50, blank=True, null=True,
    )
    phone_no = models.CharField(
        "Phone Nubmer", max_length=20, blank=True, null=True
    )
    timezone = models.ForeignKey(
        Timezone, on_delete=models.CASCADE, related_name='job_seeker_timezone', null=True, blank=True
    )
    profile_completion = models.IntegerField(default=0)
    hourly_rate = models.FloatField("Hourly Rate", blank=True, null=True)
    analytics_rate = models.FloatField("rate", blank=True, null=True)
    paid_rate = models.FloatField("You will be paid", blank=True, null=True)

    def __str__(self):
        return self.email

    def experience(self):
        if self.experience_level == "Beginner":
            return "2"
        elif self.experience_level == "Intermediate":
            return "3"
        else:
            return "5"

    class Meta:
        verbose_name_plural = "Job Seeker Management"


class EducationDetails(models.Model):
    seeker = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, related_name='job_seeker_education'
    )
    school = models.CharField(
        "School Name", max_length=100
    )
    degree = models.CharField(
        "Degree Name", max_length=100
    )
    field_of_study = models.CharField(
        "Field of Study", max_length=100
    )
    grade = models.CharField(
        "Grade", max_length=100
    )
    activities_socities = models.TextField(
        "Activities and societies"
    )
    from_year = models.CharField(
        "From Year", max_length=4
    )
    to_year = models.CharField(
        "To Year", max_length=4
    )
    description = models.TextField(
        "Description"
    )

    def __str__(self):
        return self.school

    class Meta:
        verbose_name_plural = "Education Details"


class Employment(models.Model):
    seeker = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, related_name='job_seeker_employment'
    )
    title = models.CharField(
        "Title", max_length=100
    )
    company = models.CharField(
        "Company", max_length=500
    )
    location = models.CharField(
        "location", max_length=500
    )
    MONTH = (
        ("1", "January"),
        ("2", "February"),
        ("3", "March"),
        ("4", "April"),
        ("5", "May"),
        ("6", "June"),
        ("7", "July"),
        ("8", "August"),
        ("9", "September"),
        ("10", "October"),
        ("11", "November"),
        ("12", "December"),
    )
    from_month = models.CharField(
        "From Month", max_length=15, choices=MONTH
    )
    from_year = models.CharField(
        "From Year", max_length=4
    )
    to_month = models.CharField(
        "To Month", max_length=15, choices=MONTH,
    )
    to_year = models.CharField(
        "To Year", max_length=4,
    )
    currently = models.BooleanField(default=False)
    description = models.TextField(
        "Description"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Employment History"


class UserSkillRate(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='user_skill'
    )
    skill = models.ForeignKey(
        Skills, on_delete=models.CASCADE, related_name='skill'
    )
    rate = models.CharField("Skill Rate", max_length=1, default=0)

    class Meta:
        verbose_name_plural = "Skill Rating"
        ordering = ("-rate",)


class UserLanguageRate(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='user_language'
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name='language_rate'
    )
    rate = models.CharField("Language Rate", max_length=1, default=0)


class Company(AbstractUser):
    user = models.OneToOneField(
        MyUser, on_delete=models.CASCADE, related_name='company'
    )
    company_name = models.CharField(
        "Company Name", max_length=40, blank=True, null=True
    )
    country = CountryField(blank_label='(select country)')
    industry = models.ManyToManyField(
        Industry, related_name='company_industry'
    )
    language = models.ManyToManyField(
        Language, related_name='company_language'
    )
    tools_and_language = models.ManyToManyField(
        Skills, related_name='company_tools_and_language'
    )
    profile_completion = models.IntegerField(default=0)
    rating = models.CharField(
        'Company Rating', max_length=1, blank=True, null=True, default='0'
    )

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Company Management"


class JobManagement(models.Model):

    job_name = models.CharField(max_length=500)
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company_name_jobmanagement', null=True, blank=True
    )
    area = models.ManyToManyField(
        Area, related_name='post_job_area'
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    tools_and_language = models.ManyToManyField(
        Skills, related_name='post_job_tools_and_language_jobmanagement'
    )
    language = models.ManyToManyField(
        Language, related_name='post_job_language_jobmanagement'
    )
    country = models.ManyToManyField(
        Country, related_name='job_country', null=True, blank=True
    )
    description = models.TextField()
    DURATION_PROJECT = (
        ("0-3", "0-3"),
        ("3-6", "3-6"),
        ("6-12", "6-12"),
        ("12+", "12+"),
    )
    duration = models.CharField(
        "Month", max_length=10, default="0-3", choices=DURATION_PROJECT)
    TYPE_OF_PROJECT = (
        ("One Time Project", "One Time Project"),
        ("On going Project", "On going Project"),
        ("To be decided", "To be decided")
    )
    type_of_project = models.CharField(
        "What type of project you have?", default="One Time Project", max_length=50, choices=TYPE_OF_PROJECT
    )
    number_of_employees = models.IntegerField(
        "Employee Needed", help_text="How much employee you need?", default=0
    )

    PAYMENT = (
        ("Pay by Hour", "Pay by Hour"),
        ("Pay by Fixed Price", "Pay by Fixed Price")
    )
    payment = models.CharField(
        "How would you like to pay?", default="Pay by Hour", max_length=50, choices=PAYMENT)
    SALARY = (
        ("$10/HR", "$10/HR"),
        ("$20/HR", "$20/HR"),
        ("$30/HR", "$30/HR"),
        ("others", "others")
    )
    credit = models.CharField(
        "Desired Salary", default="$10/HR", max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )

    def __str__(self):
        return self.job_name

    def applicant(self):
        if self.applied_job.filter(status="Applied").count():
            return True
        return False

    def applied(self):
        return self.applied_job.filter(status="Applied")

    @property
    def short_job_name(self):
        return truncatechars(self.job_name, 50)

    class Meta:
        verbose_name_plural = "Job Management"
        verbose_name = "Job Details"
        ordering = ("-created_at",)


class AppliedJobs(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='applied_user'
    )
    job = models.ForeignKey(
        JobManagement, on_delete=models.CASCADE, related_name='applied_job'
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    reason = models.TextField()
    resume = CloudinaryField(blank=True, null=True)
    STATUS = (
        ("Applied", "Applied"),
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Closed", "Closed"),
        ("Reject", "Reject"),
        ("Decline", "Decline"),
    )
    status = models.CharField(
        "Applied Job Status", default="Applied", max_length=20, choices=STATUS
    )
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    def __str__(self):
        return self.reason

    def document(self):
        if self.resume:
            return self.resume.build_url(
                width=100
            )
        return "-"

    class Meta:
        verbose_name_plural = "Applied Jobs"
        ordering = ("-updated_at",)
        unique_together = (("user", "job"),)


class ReviewRating(models.Model):
    job = models.ForeignKey(
        AppliedJobs, on_delete=models.CASCADE, related_name='applied_job_rating'
    )
    rate = models.CharField("Rating", max_length=1)
    feedback = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='reviewer'
    )
    reviewee = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='reviewee'
    )

    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    class Meta:
        verbose_name_plural = "Review and Rating"


class JobIncompletedReason(models.Model):
    job = models.ForeignKey(
        AppliedJobs, on_delete=models.CASCADE, related_name='applied_job_incomplete'
    )
    reason = models.TextField()
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    def __str__(self):
        return self.reason

    def document(self):
        if self.resume:
            return self.resume.build_url(
                width=100
            )
        return "-"

    class Meta:
        verbose_name_plural = "Applied Jobs"
        ordering = ("-updated_at",)


class FavouriteJobs(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='favourite_job_user'
    )
    job = models.ForeignKey(
        JobManagement, on_delete=models.CASCADE, related_name='favourite_job'
    )
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    class Meta:
        verbose_name_plural = "Favourite Jobs"
        ordering = ("-updated_at",)


class ChatList(models.Model):
    company = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='company_chat'
    )
    jobseeker = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='jobseeker_chat'
    )
    job = models.ForeignKey(
        JobManagement, on_delete=models.CASCADE, related_name='job'
    )
    companydeleted = models.BooleanField(default=False)
    jobseekerdeleted = models.BooleanField(default=False)
    invitation = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    def latest_chat(self):
        return self.chatlist.latest('created_at')

    class Meta:
        verbose_name_plural = "Chat List"
        ordering = ('-chatlist',)
        unique_together = ['company','jobseeker','job']


class Chats(models.Model):
    chat = models.ForeignKey(
        ChatList, on_delete=models.CASCADE, related_name='chatlist'
    )
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='chatsender'
    )
    receiver = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='chatreceiver'
    )
    message = models.CharField(
        "Message", max_length=1000, blank=True, default=True
    )
    msg_type = models.CharField(
        'Type', max_length=20, default="text"
    )
    attachment = models.BooleanField(
        default=False
    )
    edited = models.BooleanField(
        default=False
    )
    deleted = models.BooleanField(
        default=False
    )
    read = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    class Meta:
        verbose_name_plural = "Chats"
        ordering = ('created_at',)


# class MessageNotification(models.Model):
#     sender = models.ForeignKey(
#         MyUser, on_delete=models.CASCADE, related_name='messagesender'
#     )
#     receiver = models.ForeignKey(
#         MyUser, on_delete=models.CASCADE, related_name='messagereceiver'
#     )
#     chat = models.ForeignKey(
#         ChatList, on_delete=models.CASCADE, related_name='message_chat_list'
#     )
#     message = models.CharField(
#         "Message", max_length=2000
#     )

#     created_at = models.DateTimeField(
#         "Created Date", auto_now_add=True
#     )
#     updated_at = models.DateTimeField(
#         "Updated Date", auto_now=True
#     )

#     class Meta:
#         verbose_name_plural = "Message Notification"
#         ordering = ("-created_at",)


class NotificationList(models.Model):
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='notificationsender'
    )
    receiver = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='notificationreceiver'
    )
    message = models.CharField(
        "Message", max_length=2000
    )
    TYPE = (
        ("Applied Job", "Applied Job"),
        ("Approved Job", "Approved Job"),
        ("Completed Job", "Completed Job"),
        ("Pending Job", "Pending Job"),
        ("Closed Job", "Closed Job"),
        ("Declined Job", "Declined Job"),
        ("Chat", "Chat"),
    )
    type = models.CharField(
        "Notification Type", max_length=20, blank=True, null=True, choices=TYPE
    )
    job = models.ForeignKey(
        AppliedJobs, on_delete=models.CASCADE, related_name='job_notification'
    )
    link = models.CharField(
        "Link", max_length=2000, blank=True, null=True
    )
    seen = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    class Meta:
        verbose_name_plural = "Notifications List"
        ordering = ("-created_at",)


class Profession(Name):

    class Meta:
        verbose_name_plural = "Analytic's Profession"
        ordering = ('id',)


class Career(models.Model):
    email = models.EmailField("User Email", unique=False, max_length=50)
    first_name = models.CharField(
        "First Name", max_length=40, blank=True, null=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, blank=True, null=True
    )
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, related_name='carrer_profession'
    )
    message = models.TextField(
        "Message", blank=True, null=True
    )
    mobile_number = models.CharField(
        "Mobile Number", max_length=15, blank=True, null=True
    )
    resume = CloudinaryField(
        "Resume", resource_type='auto'
    )

    @property
    def short_message(self):
        return truncatechars(self.message, 50)

    def __str__(self):
        return self.email


class ContactUs(models.Model):
    email = models.EmailField(
        "User Email"
    )
    first_name = models.CharField(
        "First Name", max_length=40, blank=True, null=True
    )
    last_name = models.CharField(
        "Last Name", max_length=40, blank=True, null=True
    )
    message = models.TextField(
        "Message", blank=True, null=True
    )
    mobile_number = models.CharField(
        "Mobile Number", max_length=15, blank=True, null=True
    )

    def __str__(self):
        return self.email


class BoardMember(models.Model):
    email = models.EmailField(
        "User Email", unique=True, max_length=50
    )
    avatar = CloudinaryField(
        "Member Image", blank=True, null=True
    )
    first_name = models.CharField(
        "First Name", max_length=40
    )
    last_name = models.CharField(
        "Last Name", max_length=40, blank=True, null=True
    )
    designation = models.CharField(
        "Designation", max_length=100
    )
    mobile_number = models.CharField(
        "Mobile Number", max_length=15, blank=True, null=True
    )
    city_country = models.CharField(
        "City and Country", max_length=100
    )

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = "Board Members"


class TransactionManagement(models.Model):

    recipient = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='recipient'
    )
    sender = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='sender'
    )
    total = models.FloatField(default=0.0)
    recipient_share = models.FloatField()
    analytics_share = models.FloatField()
    job = models.ForeignKey(
        AppliedJobs, on_delete=models.CASCADE, related_name='transaction_job'
    )
    key = models.CharField(
        "Paypal Transaction Key", max_length=40
    )
    STATUS = (
        ("PENDING", "PENDING"),
        ("COMPLETED", "COMPLETED"),
    )
    status = models.CharField(
        "Payment Status", max_length=15, default="PENDING", choices=STATUS
    )
    PAYMENT = (
        ("ADVANCE", "ADVANCE"),
        ("ESCROW", "ESCROW"),
    )
    payment = models.CharField(
        "Payment Type", max_length=10, default="ADVANCE", choices=PAYMENT
    )
    released = models.BooleanField("Payment Release", default=False)
    created_at = models.DateTimeField(
        "Created Date", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Updated Date", auto_now=True
    )

    class Meta:
        verbose_name_plural = "Transaction Management"
