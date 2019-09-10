from django.contrib import admin
from .models import AboutUs, FAQ, TermsAndConditions, HowitWorks
from .forms import *
from django.utils.safestring import mark_safe
# Register your models here.


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['avatar','overview', 'overview_description',
                     'mission', 'mission_description', 'Action']
    list_display_links = None

    form = AboutUsForm

    def has_add_permission(self, request):
        if AboutUs.objects.all().exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """method to remove  delete action from admin """
        # Disable delete
        actions = super(AboutUsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/staticmanagement/aboutus/{}/change/'>Edit</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))


admin.site.register(AboutUs, AboutUsAdmin)


class FAQAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = ['question', 'Action']
    form = FAQForm

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/staticmanagement/faq/{}/change/'>View</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(FAQ, FAQAdmin)

class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = ['title', 'Action']
    form = TermsAndConditionsForm

    def title(self,request):
        return "Terms & Conditions"

    def has_add_permission(self, request):
        if TermsAndConditions.objects.all().exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/staticmanagement/termsandconditions/{}/change/'>Edit</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))

    def get_actions(self, request):
        """method to remove  delete action from admin """
        # Disable delete
        actions = super(TermsAndConditionsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
        
admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)


class HowitWorksAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = ['title','content', 'Action']
    form = HowitWorksForm

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/staticmanagement/howitworks/{}/change/'>Edit</a>".format(obj.id)+ "    " + "<a class='button btn' style='color:white; padding:0 1rem; ' href='/admin/staticmanagement/howitworks/{}/delete/'>Delete</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))

    def get_actions(self, request):
        """method to remove  delete action from admin """
        # Disable delete
        actions = super(HowitWorksAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(HowitWorks, HowitWorksAdmin)


admin.site.register(Tags)



class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'Action']
    list_display_links = None

    def title(self,request):
        return "Privacy Policy"

    def has_add_permission(self, request):
        if PrivacyPolicy.objects.all().exists():
            return False
        return True


    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        """method to remove  delete action from admin """
        # Disable delete
        actions = super(PrivacyPolicyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/staticmanagement/privacypolicy/{}/change/'>Edit</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))

admin.site.register(PrivacyPolicy,PrivacyPolicyAdmin)



class ReferFriendAdmin(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(ReferFriend,ReferFriendAdmin)



class WhoAreWeAdmin(admin.ModelAdmin):

    list_display = ['Content','Action']

    def has_add_permission(self, request):
        if WhoAreWe.objects.all().exists():
            return False
        return True

    def Content(self, obj):
        return "Who we are!!!"

    def Action(self, obj):
        if obj.id:

            return mark_safe("<a class='button btn' style='color:white;' href='/admin/staticmanagement/whoarewe/{}/change/'>Edit</a>".format(obj.id))
        else:
            social_button = '<a  href="#">-</a>'
            return mark_safe(u''.join(social_button))
admin.site.register(WhoAreWe,WhoAreWeAdmin)