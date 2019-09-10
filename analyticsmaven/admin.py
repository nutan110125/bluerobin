from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe
from .forms import *
admin.site.empty_value_display = '-'
admin.site.site_url = 'http://ec2-13-250-224-209.ap-southeast-1.compute.amazonaws.com:8002/'

class SkillsAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/skills/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/skills/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Skills, SkillsAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/area/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/area/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Area, AreaAdmin)


class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/industry/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/industry/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Industry, IndustryAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/country/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/country/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Country, CountryAdmin)


class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/profession/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/profession/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Profession, ProfessionAdmin)


class TimezoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/timezone/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/timezone/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Timezone, TimezoneAdmin)


class HoursAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/hours/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/hours/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Hours, HoursAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'is_active', 'created_by', 'Action')
    list_display_links = None
    list_per_page = 50

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/language/{} /change/'>Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/analyticsmaven/language/{}/delete/'>Delete</a>".format(obj.id))

        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(Language, LanguageAdmin)


class AppliedJobInline(admin.StackedInline):
    """Show TIme Details"""

    def has_add_permission(self, request):
        return False
    model = AppliedJobs


class EducationInline(admin.StackedInline):
    """Show TIme Details"""
    extra = 0
    model = EducationDetails


class EmploymentInline(admin.StackedInline):
    """Show TIme Details"""

    form = EmploymentAdminForm


    extra = 0
    model = Employment


class JobSeekerManagementAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'email',
                    'phone_no', 'status', 'created_at', 'Action']
    list_display_links = None
    list_per_page = 50
    form = JobSeekerForm
    inlines = (EducationInline, EmploymentInline,)

    def status(self, obj):
        return obj.user.is_active

    def get_queryset(self, request):
        qs = super(JobSeekerManagementAdmin, self).get_queryset(request)
        return qs.filter(user__user_type='Job Seeker')

    def save_model(self, request, obj, form, change):
        '''docstring'''
        if "email" in form.changed_data:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('contact_number')
            try:
                user, created = MyUser.objects.get_or_create(
                    email=email
                )
                user.set_password(password)
                user.save()
                obj.user = user
            except Exception as e:
                print("Exception as e---->>>", e)
                pass
        obj.save()

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; width: 104px; ' href='/admin/analyticsmaven/jobseeker/{}/change/'>View/Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; width: 104px;' href='/admin/analyticsmaven/jobseeker/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

    def delete_model(modeladmin, request, obj):
        user = MyUser.objects.get(email=obj.email)
        user.delete()
        return True


admin.site.register(JobSeeker, JobSeekerManagementAdmin)


class JobInline(admin.StackedInline):
    """Show TIme Details"""
    extra = 0
    model = JobManagement


class CompanyManagementAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'email',
                    'contact_number', 'status', 'created_at', 'Action']
    list_display_links = None
    list_per_page = 50
    form = CompanyForm
    inlines = [JobInline]

    def status(self, obj):
        return obj.user.is_active

    def get_queryset(self, request):
        qs = super(CompanyManagementAdmin, self).get_queryset(request)
        return qs.filter(user__user_type='Company')

    def save_model(self, request, obj, form, change):
        '''docstring'''
        if "email" in form.changed_data:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('contact_number')
            try:
                user, created = MyUser.objects.get_or_create(
                    email=email
                )
                user.set_password(password)
                user.user_type = 'Company'
                user.save()
                obj.user = user
                obj.save()
            except Exception as e:
                print("Exception as e---->>>", e)
                pass

    def delete_model(modeladmin, request, obj):
        user = MyUser.objects.get(email=obj.email)
        user.delete()
        return True

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;  width: 104px; ' href='/admin/analyticsmaven/company/{}/change/'>View/Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem;  width: 104px;' href='/admin/analyticsmaven/company/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

    class Meta:
        verbose_name = "Company Management"
        verbose_name_plural = "Company Management"


admin.site.register(Company, CompanyManagementAdmin)


class JobManagementAdmin(admin.ModelAdmin):
    list_display = (
        'short_job_name', 'company_name', 'number_of_employees', 'is_active', 'created_at', 'Action'
    )
    search_fields = ("job_name",)
    list_per_page = 50
    inlines = [AppliedJobInline]

    def Action(self, obj):
        if obj.id:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem; width: 104px;' href='/admin/analyticsmaven/jobmanagement/{}/change/'>View/Edit</a>".format(obj.id)
                             + "    " + "<a class='button btn' style='color:white; padding:0 1rem; width: 104px; ' href='/admin/analyticsmaven/jobmanagement/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))

    def number_of_applicants(self, obj):
        pass


admin.site.register(JobManagement, JobManagementAdmin)


class AnalyticsRateAdmin(admin.ModelAdmin):
    list_display = ['fees', 'Action']
    list_display_links = None

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/analyticsmaven/analyticsrate/{}/change/'>Edit</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))

    def has_add_permission(self, request):
        if AnalyticsRate.objects.all().exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    # def get_actions(self, request):
    #     """method to remove  delete action from admin """
    #     actions = super(AnalyticsRateAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions


admin.site.register(AnalyticsRate, AnalyticsRateAdmin)


class SkillRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'rate']




class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'user_type', 'sign_up', 'is_active']


admin.site.register(MyUser, MyUserAdmin)


class AppliedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'status', 'created_at', 'updated_at']
    readonly_fields = ('Resume_file',)

    def Resume_file(self, obj):
        if obj.resume:
            return mark_safe('<embed src="{}" width="100%" height="800"/>'.format(obj.resume.url))
        return "-"

admin.site.register(AppliedJobs, AppliedJobAdmin)


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'rate', 'feedback', 'created_at']


admin.site.unregister(Group)


class CareerAdmin(admin.ModelAdmin):

    form = CareerAdminModelForm
    list_display = ['email', 'first_name', 'mobile_number', 'profession',"short_message"]
    readonly_fields = ('Resume_file',)

    def Resume_file(self, obj):
        if obj.resume:
            return mark_safe('<embed src="{}" width="100%" height="800"/>'.format(obj.resume.url))
        return "-"


admin.site.register(Career,CareerAdmin)


class ChatListAdmin(admin.ModelAdmin):
    list_display = ['company', 'jobseeker', 'job']


admin.site.register(ChatList, ChatListAdmin)


class ChatsAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'chat', 'message']


admin.site.register(Chats, ChatsAdmin)


class BoardMemberAdmin(admin.ModelAdmin):

    form = BoardMemberAdminModelForm

    list_display = ['first_name', 'email',
                    'designation', 'mobile_number', 'city_country']


admin.site.register(BoardMember, BoardMemberAdmin)


class NotificationListAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver',
                    'message', 'type']




class TransactionManagementAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'job', 'total',
                    'recipient_share', 'analytics_share', 'status', 'payment', 'released', 'created_at', 'Action']

    def Action(self, obj):
        if obj.payment == "ESCROW" and obj.status == "COMPLETED" and not obj.released:
            return mark_safe("<a class='button btn' style='color:white; padding:0 1rem;  width: 104px;' href='/release-payment/{}'>Release</a>".format(obj.id))
        else:
            social_button = '<a  href="#">---</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(TransactionManagement, TransactionManagementAdmin)
