import os
import time
import ast
from datetime import date, timedelta
import datetime
from itertools import chain
from functools import reduce
from cloudinary.uploader import upload

from django.views import View

from django.shortcuts import render, redirect,HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site

from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q, Avg

from rest_framework.views import APIView
from rest_framework import status

from staticmanagement.models import *
from .send_link import send_link, send_mail, send_applied_job_mail, send_completed_job_mail, post_job_successfully_mail, send_pending_job_mail, delete_job_successfully_mail
from .profile_percentage import percentage
from .company_percentage import company_percentage
from .models import *
from .forms import *
from .utils import user_experience_level
from .paypal import *
# from .adminpaypal import *
############### Employee Register Management URL ###############

class HomeView(View):
    def get(self, request, uuid=None):
        if request.user.id:
            return redirect("analyticsmaven:dashboard")
        return render(request, "index.html")

############### Looking for a job - Home Page ###############


class LookingForJob(View):
    def get(self, request):
        all_jobs = JobManagement.objects.all()
        if 'qf' in request.GET:
            all_jobs = all_jobs.filter(
                job_name__icontains=request.GET.get('qf')
            )
        if 'dqf' in request.GET:
            current = date.today()
            if request.GET.get('dqf') == "today":
                all_jobs = all_jobs.filter(
                    created_at__date=current
                )
            elif request.GET.get('dqf') == "yesterday":
                all_jobs = all_jobs.filter(
                    created_at__date=current - timedelta(1)
                )
            elif request.GET.get('dqf') == "week":
                current = current - timedelta(7)
                weekday = current.weekday()
                start_delta = datetime.timedelta(days=weekday)
                start = current - start_delta
                end = start + datetime.timedelta(days=6)
                all_jobs = all_jobs.filter(
                    created_at__date__gte=start,
                    created_at__date__lt=end
                )
            elif request.GET.get('dqf') == "month":
                end = current.replace(day=1)
                end = end - timedelta(days=1)
                start = end.replace(day=1)
                all_jobs = all_jobs.filter(
                    created_at__date__gte=start,
                    created_at__date__lt=end
                )
        if 'tqf' in request.GET:
            print("Time Query Filter", request.GET.get('tqf', None))

        if 'pqf' in request.GET:
            all_jobs = all_jobs.filter(
                credit=request.GET.get('pqf')
            )
        if 'tpqf' in request.GET:
            all_jobs = all_jobs.filter(
                type_of_project=request.GET.get('tpqf')
            )
        if 'mqf' in request.GET:
            all_jobs = all_jobs.filter(
                duration=request.GET.get('mqf')
            )
        if 'eqf' in request.GET:
            pass
            # all_jobs = all_jobs.filter(
            #     experience_level=request.GET.get('eqf')
            # )
        page = request.GET.get('page')
        paginator = Paginator(all_jobs, 15)
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
        return render(request, "looking-for-job.html",{'jobs':jobs})

############### Looking for a jobseeker - Home Page ###############

class EmployersList(View):
    def get(self, request):
        analytic_professional = JobSeeker.objects.filter(user__is_active=True)
        page = request.GET.get('page')
        paginator = Paginator(analytic_professional, 15)
        try:
            professional = paginator.page(page)
        except PageNotAnInteger:
            professional = paginator.page(1)
        except EmptyPage:
            professional = paginator.page(paginator.num_pages)
        return render(request, "employers.html",{'professional':professional})


############### Employee Register Management URL ###############


class Registration(View):
    '''View for saving user email-Registration'''

    def post(self, request):
        params = request.POST
        print("Params", params)
        try:
            MyUser.objects.get(email=params['email'])
            return render(request, "index.html", {"type": "login", "message": "Email already registered, you can login to your account."})
        except Exception as e:
            print("Exception as e", e)
            form = RegistrationForm(params or None)
            if form.is_valid():
                user = form.save()
                user.set_password(time.time())
                user.save()
                return redirect(
                    "analyticsmaven:registration-details", user.uuid
                )


class UserImage(APIView):
    '''API for saving user image'''
    authentication_classes = []

    def post(self, request):
        params = request.POST
        instance = MyUser.objects.get(uuid=params['uuid'])
        if 'avatar' in params and params['avatar']:
            image = upload(params['avatar'])
            instance.avatar = image['url']
            instance.save()
        return JsonResponse({"status": 200})


class Attachment(APIView):
    authentication_classes = []
    def post(self,request):
        params = request.POST
        attachment = cloudinary.uploader.upload(params['attachment'])
        url = attachment.get('url')
        return JsonResponse({"status": 200,'url':url})


class RegistrationDetails(View):
    '''View for Step1 Registration'''

    def get(self, request, uuid=None):
        try:
            user = MyUser.objects.get(uuid=uuid)
            if user.user_type == "Company":
                return redirect("analyticsmaven:company-registration", user.uuid)
            return render(request, "job_seeker/step1.html", {"user": user})
        except Exception as e:
            print("Exceptino as e", e)
            return render(request, "index.html")

    def post(self, request, uuid=None):
        params = request.POST
        instance = MyUser.objects.get(uuid=uuid)
        form = RegistrationDetailForm(params, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(params['password'])
            user.save()
            jobseeker, created = JobSeeker.objects.get_or_create(
                user=user
            )
            jobseeker.email = user.email
            jobseeker.first_name = user.first_name
            jobseeker.last_name = user.last_name
            jobseeker.save()
            percentage(instance)
            if request.user.is_authenticated() and instance.is_active:
                return redirect("analyticsmaven:dashboard")
            return redirect("analyticsmaven:user-skills", user.uuid)
        return render(request, "job_seeker/step1.html", {"form": form, "user": instance})


class UserSkill(View):
    '''Step2 Job Seeker Registration'''

    def get(self, request, uuid=None):
        try:
            user = MyUser.objects.get(uuid=uuid)
            areas = Area.objects.filter(is_active=True)
            industrys = Industry.objects.filter(is_active=True)
            skills = Skills.objects.filter(is_active=True)
            if user.job_seeker.area:
                area = Area.objects.filter(
                    is_active=False, name__in=[i.name for i in user.job_seeker.area.all()])
                areas = list(chain(areas, area))
            if user.job_seeker.industry:
                industry = Industry.objects.filter(
                    is_active=False, name__in=[i.name for i in user.job_seeker.industry.all()])
                industrys = list(chain(industrys, industry))
            if user.job_seeker.tools_and_language:
                skill = Skills.objects.filter(
                    is_active=False, name__in=[i.name for i in user.job_seeker.tools_and_language.all()])
                skills = list(chain(skills, skill))
            return render(request, "job_seeker/step2.html", {
                "user": user,
                "areas": areas,
                "industries": industrys,
                "skills": skills
            })
        except Exception as e:
            print("Exception", e)
            return render(request, "index.html")

    def post(self, request, uuid=None):
        params = request.POST
        print("Parameters", params)
        user = MyUser.objects.get(uuid=uuid)
        if "skill" in params and request.POST.getlist('skill'):
            skillList = []
            for skill in request.POST.getlist('skill'):
                try:
                    skillObj = Skills.objects.get(id=skill)
                except Exception as e:
                    skillObj, created = Skills.objects.get_or_create(
                        name=skill.title()
                    )
                    skillObj.is_active = True
                    skillObj.created_by = "USER"
                    skillObj.save()
                created_skill, created = UserSkillRate.objects.get_or_create(
                    user=user,
                    skill=skillObj
                )
                skillList.append(skillObj.id)
            user.job_seeker.tools_and_language = skillList
        if "industry" in params and request.POST.getlist('industry'):
            industryList = []
            for industry in request.POST.getlist('industry'):
                try:
                    industryObj = Industry.objects.get(id=industry)
                except Exception as e:
                    industryObj, created = Industry.objects.get_or_create(
                        name=industry.title()
                    )
                    industryObj.is_active = True
                    industryObj.created_by = "USER"
                    industryObj.save()
                industryList.append(industryObj.id)
            user.job_seeker.industry = industryList
        if "area" in params and request.POST.getlist('area'):
            areaList = []
            for area in request.POST.getlist('area'):
                try:
                    areaObj = Area.objects.get(id=area)
                except Exception as e:
                    areaObj, created = Area.objects.get_or_create(
                        name=area.title()
                    )
                    areaObj.is_active = True
                    areaObj.created_by = "USER"
                    areaObj.save()
                areaList.append(areaObj.id)
            user.job_seeker.area = areaList
        user.job_seeker.save()
        percentage(user)
        if request.user.is_authenticated() and user.is_active:
            return redirect("analyticsmaven:dashboard")
        return redirect("analyticsmaven:user-details", user.uuid)


class UserDetails(View):
    '''Step3 Job Seeker Registration'''

    def get(self, request, uuid=None):
        try:
            user = MyUser.objects.get(uuid=uuid)
            return render(request, "job_seeker/step3.html", {"user": user})
        except Exception as e:
            print("Exception as e",e)
            return render(request, "index.html")

    def post(self, request, uuid=None):
        params = request.POST
        user = MyUser.objects.get(uuid=uuid)
        user.job_seeker.professional_title = params['professional_title']
        user.job_seeker.overview = params['overview']
        user.job_seeker.save()
        if params['paypal']:
            user.paypal_email = params['paypal']
            user.save()
        percentage(user)
        if request.user.is_authenticated() and user.is_active:
            return redirect("analyticsmaven:dashboard")
        if not request.user.is_authenticated() and not user.is_active:
            send_mail(request, user)
        return render(request, "job_seeker/step3.html", {"user": user, "type": "success"})


class UserSkillRating(APIView):
    def post(self, request):
        params = request.POST
        print("Params", params)
        skill_rate, created = UserSkillRate.objects.get_or_create(
            user_id=params['user'],
            skill_id=params['skill']
        )
        skill_rate.rate = params['rate']
        skill_rate.save()
        user_experience_level(request, params)
        return JsonResponse({"status": 200})

############### Company Register Management URL ###############


class CompanyRegistration(View):

    def get(self, request, uuid=None):
        user = MyUser.objects.get(uuid=uuid)
        return render(request, 'company/company-step1.html', {"user": user})

    def post(self, request, uuid=None):
        instance = MyUser.objects.get(uuid=uuid)
        if request.user.id:
            form = CompanyRegisterUpdateForm(request.POST, instance=instance)
        else:
            form = CompanyRegisterForm(request.POST, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            if 'password' in request.POST and request.POST['password']:
                user.set_password(request.POST['password'])
            user.save()
            company, created = Company.objects.get_or_create(
                user=user
            )
            company.email = user.email
            company.company_name = user.first_name
            company.save()
            company_percentage(instance)
            return redirect("analyticsmaven:industry-type", user.uuid)
        print(form.errors)
        return render(request, 'company/company-step1.html')


class CompanyIndustryType(View):
    def get(self, request, uuid=None):
        try:
            user = MyUser.objects.get(uuid=uuid)
            company_percentage(user)
            return render(request, "company/company-step2.html", {"user": user})
        except Exception as e:
            return render(request, "company/company-step1.html")

    def post(self, request, uuid=None):
        instance = MyUser.objects.get(uuid=uuid)
        params = request.POST
        user = MyUser.objects.get(uuid=uuid)
        print(request.POST.getlist('industry'))
        if "industry" in params and request.POST.getlist('industry'):
            industryList = []
            for industry in request.POST.getlist('industry'):
                try:
                    industryObj = Industry.objects.get(id=industry)
                except Exception as e:
                    print("Industry", industry)
                    industryObj, created = Industry.objects.get_or_create(
                        name=industry.title()
                    )
                    industryObj.is_active = True
                    industryObj.created_by = "USER"
                    industryObj.save()
                industryList.append(industryObj.id)
            user.company.industry = industryList
        user.company.save()
        company_percentage(instance)
        if request.user and request.user.is_authenticated and request.user.id:
            return redirect('analyticsmaven:company-profile')
        else:
            send_mail(request, user)
            return render(request, 'company/company-step2.html', {"user": user, 'type': 'success'})

############### Profile Activation Management URL ###############


class Activate(View):
    def get(self, request, uuid=None):
        try:
            user = MyUser.objects.get(uuid=uuid)
            if user:
                user.is_active = True
                user.save()
                return redirect("analyticsmaven:login")
        except Exception as e:
            print("Exception as e", e)

############### User Management URL ###############


class Login(View):
    '''View for user login'''

    def get(self, request):
        return render(request, "index.html", {"type": "login"})

    def post(self, request, uuid=None):
        params = request.POST
        print("Parameters",params)
        try:
            user = MyUser.objects.get(email=request.POST['email'])
            print("user",user)
            if user.check_password(request.POST['password']) and not user.is_active:
                return render(request, "index.html", {
                    "login_failed_message": "We already have a account with this email you need to activate your Account", 
                    "type": "login"
                })
        except Exception as e:
            print("Exception as e",e)
            pass
        user = authenticate(
            email=request.POST['email'],
            password=request.POST['password']
        )
        print("User",user)
        if user is not None and not user.is_superuser:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect("analyticsmaven:dashboard")
        elif user is not None and user.is_superuser:
            login(request, user)
            return redirect("/admin")
        return render(request, "index.html", {"login_failed_message": "Please enter valid credentials.", "type": "login"})


@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("analyticsmaven:home")


class Forgot(View):
    def get(self, request, uuid=None):
        user = MyUser.objects.get(uuid=uuid)
        return render(request, "forgot.html", {"user": user})


class ForgotPasswordUser(View):
    def post(self, request):
        try:
            user = MyUser.objects.get(email=request.POST['email'])
            if user:
                send_link(request, user)
                return render(request, 'index.html', {
                    "type": "linksentsuccess"
                    })
            else:
                message = "Unable to locate your Email.Please enter your registered Email ID."
                return render(request, 'index.html', {
                    "message": message
                })
        except Exception as e:
            print("Exception as e:", e)
            return render(request, 'index.html', {
                'type': 'incorrect_email',
                'error': 'Unable to locate your Email.Please enter your registered Email ID.'
            })


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def post(self, request, uuid=None):
        params = request.POST
        if not request.user.check_password(params['old_password']):
            old_error = "Your password did not match, please enter correct password"
            return render(request, "dashboard.html", {"old_error": old_error, "type": "old_error"})
        form = ResetPasswordForm(params)
        if form.is_valid():
            request.user.set_password(params['password'])
            request.user.save()
            message = "Your Password is Changed, Please Login to continue."
            logout(request)
            return render(request, "index.html", {"message": message, "type": "login"})
        return render(request, "dashboard.html", {"type": "old_error", "form": form})


@method_decorator(login_required, name='dispatch')
class ViewProfile(View):
    def get(self, request):
        return render(request, 'profile.html')


@method_decorator(login_required, name='dispatch')
class EditProfile(View):
    def get(self, request):
        return render(request, 'edit-profile.html')

    def post(self, request):
        try:
            skills = Skills.objects.all()
            params = request.POST
            print(request.user)
            print(params)
            print("params", params['country'])
            jobseeker = JobSeeker.objects.get(user=request.user)
            form = EditProfileForm(params['country'])
            if form.is_valid():
                user = form.save()
                return render(request, 'profile.html', {"user": user, "skills": skills})
            print(form.errors)
        except Exception as e:
            print("Exception as e :", e)
            return render(request, "dashboard.html", {"user": request.user})


class ResetUserPassword(View):
    def post(self, request, uuid=None):
        print("param", request.POST)
        user = MyUser.objects.get(uuid=uuid)
        if request.POST['password'] == request.POST['confirm_password']:

            if user:
                user.set_password(request.POST['password'])
                user.save()
                reset_pass_message = "Password Changed Successfully, You Can Login Now. "
                return render(request, 'index.html', {"reset_pass_message": reset_pass_message, "type": "login"})
            message = "User Does Not Exist"
            return render(request, 'index.html', {"message": message})
        message = "New Password & Confirm Password Did Not Match"
        return render(request, 'forgot.html', {"message": message, "user": user})

############### Employee Profile Management URL ###############


@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    def get(self, request):
        if  request.user.is_superuser:
            logout(request)
            return redirect('analyticsmaven:login')            
        elif request.user.user_type == 'Company':
            tab = "tab1"
            company = JobManagement.objects.filter(
                company_name__company_name=request.user.first_name,is_active=True)
            paginator = Paginator(company, 5)
            if 'pages' in request.GET:
                page = request.GET.get('pages')
                tab = "tab2"
                
            else:
                page = request.GET.get('page')
                tab = "tab1"
            try:
                companypage = paginator.page(page)
            except PageNotAnInteger:
                companypage = paginator.page(1)
            except EmptyPage:
                companypage = paginator.page(paginator.num_pages)
            company_percentage(request.user)
            # seeker = JobSeeker.objects.filter(
            #     user__is_active=True,tools_and_language__in=request.user.company.company_name_jobmanagement.values_list('tools_and_language', flat=True), industry__in= request.user.company.industry.all().values_list('id', flat=True),user__is_superuser=False).order_by('user').distinct()
            job_ids = company.values_list('id',flat=True)
            applied_job_seeker = AppliedJobs.objects.filter(job_id__in=job_ids,status="Applied").values_list('user_id',flat=True)
            seeker = JobSeeker.objects.filter(
                user_id__in= applied_job_seeker,user__is_active=True,user__is_superuser=False).order_by('user').distinct()
            paginator = Paginator(seeker, 6)
            page = request.GET.get('page')
            try:
                job_seeker = paginator.page(page)
            except PageNotAnInteger:
                job_seeker = paginator.page(1)
            except EmptyPage:
                job_seeker = paginator.page(paginator.num_pages)
            return render(request, 'jobs.html', {"job_seeker": job_seeker, "companypage": companypage, "tab": tab})
        percentage(request.user)
        if request.user.job_seeker.profile_completion < 50:
            return render(request, "complete-profile.html", {
                "section": "personal-details",  
            })
        # For Active Jobs
        matched = JobManagement.objects.filter(
            tools_and_language__in=request.user.job_seeker.tools_and_language.all(), is_active=True).distinct()
        if 'qf' in request.GET:
            matched = matched.filter(
                job_name__icontains=request.GET.get('qf')
            )
        if 'dqf' in request.GET:
            current = date.today()
            if request.GET.get('dqf') == "today":
                matched = matched.filter(
                    created_at__date=current
                )
            elif request.GET.get('dqf') == "yesterday":
                matched = matched.filter(
                    created_at__date=current - timedelta(1)
                )
            elif request.GET.get('dqf') == "week":
                current = current - timedelta(7)
                weekday = current.weekday()
                start_delta = datetime.timedelta(days=weekday)
                start = current - start_delta
                end = start + datetime.timedelta(days=6)
                matched = matched.filter(
                    created_at__date__gte=start,
                    created_at__date__lt=end
                )
            elif request.GET.get('dqf') == "month":
                end = current.replace(day=1)
                end = end - timedelta(days=1)
                start = end.replace(day=1)
                matched = matched.filter(
                    created_at__date__gte=start,
                    created_at__date__lt=end
                )
        if 'tqf' in request.GET:
            print("Time Query Filter", request.GET.get('tqf', None))

        if 'pqf' in request.GET:
            matched = matched.filter(
                credit=request.GET.get('pqf')
            )
        if 'tpqf' in request.GET:
            matched = matched.filter(
                type_of_project=request.GET.get('tpqf')
            )
        if 'mqf' in request.GET:
            matched = matched.filter(
                duration=request.GET.get('mqf')
            )
        if 'eqf' in request.GET:
            pass
            # matched = matched.filter(
            #     experience_level=request.GET.get('eqf')
            # )
        paginator = Paginator(matched, 5)
        page = request.GET.get('page')
        try:
            matched_jobs = paginator.page(page)
        except PageNotAnInteger:
            matched_jobs = paginator.page(1)
        except EmptyPage:
            matched_jobs = paginator.page(paginator.num_pages)
        return render(request, "dashboard.html", {"matching_jobs": matched_jobs, "tab": "0"})


class CompleteProfile(View):
    def get(self, request):
        # user_experience_level(request)
        return render(request, "complete-profile.html", {
            "section": "personal-details",
        })


class AddEducation(View):
    def get(self, request):
        percentage(request.user)
        return render(request, "complete-profile.html", {"section": "personal-details"})

    def post(self, request):
        params = request.POST
        print("Params", params)
        form = EducationForm(params or None)
        if form.is_valid():
            form.save()
            percentage(request.user)
            return redirect('analyticsmaven:complete-profile')
        print(form.errors)
        return render(request, 'complete-profile.html', {
            "form": form,
            "type": "education",
            "section": "personal-details"
        })


class DeleteEducation(View):
    def get(self, request, pk=None):
        try:
            EducationDetails.objects.get(id=pk).delete()
        except:
            pass
        return redirect('analyticsmaven:complete-profile')


class AddEmployment(View):
    def get(self, request):
        percentage(request.user)
        return render(request, "complete-profile.html",  {"section": "personal-details"})

    def post(self, request):
        params = request.POST
        print("Params", params)
        form = EmploymentForm(params or None)
        if form.is_valid():
            form.save()
            percentage(request.user)
            return redirect('analyticsmaven:complete-profile')
        print(form.errors)
        return render(request, 'complete-profile.html', {
            "form": form,
            "type": "employment",
            "section": "personal-details"
        })


class DeleteEmployment(View):
    def get(self, request, pk=None):
        try:
            Employment.objects.get(id=pk).delete()
        except:
            pass
        return redirect('analyticsmaven:complete-profile')


@method_decorator(login_required, name='dispatch')
class PersonalDetails(View):
    def post(self, request):
        percentage(request.user)
        params = request.POST
        print("User Language Parameters", request.POST.getlist('language'))
        if "language" in params and request.POST.getlist('language'):
            languageList = []
            for language in request.POST.getlist('language'):
                try:
                    languageObj = Language.objects.get(id=language)
                except Exception as e:
                    languageObj, created = Language.objects.get_or_create(
                        language=language.title()
                    )
                    languageObj.is_active = False
                    languageObj.created_by = "USER"
                    languageObj.save()
                languageList.append(languageObj.id)
            request.user.job_seeker.language_known = languageList
            request.user.job_seeker.save()
        return redirect("analyticsmaven:set-location")


@method_decorator(login_required, name='dispatch')
class UserLanguageRating(APIView):
    def post(self, request):
        params = request.POST
        print("User Rating Parameters", params)
        try:
            language = Language.objects.get(id=params['language'])
        except:
            language, created = Language.objects.get_or_create(
                language=params['language'].title()
            )
            language.is_active = False
            language.created_by = "USER"
            language.save()
        language_rate, created = UserLanguageRate.objects.get_or_create(
            user_id=params['user'],
            language=language
        )
        language_rate.rate = params['rate']
        language_rate.save()
        return JsonResponse({"status": 200})


@method_decorator(login_required, name='dispatch')
class SetLocation(View):
    def get(self, request):
        return render(request, 'complete-profile.html', {"section": "set-location"})

    def post(self, request):
        params = request.POST
        print("Parameters", params)
        if params['country']:
            try:
                country = Country.objects.get(id=params['country'])
            except Exception as e:
                print("Exception as e", e)
                mutable = request.POST._mutable
                request.POST._mutable = True

                country, created = Country.objects.get_or_create(
                    name=params['country'].title()
                )
                country.is_active = False
                country.created_by = "USER"
                country.save()
                request.POST['country'] = country.id
                request.POST._mutable = mutable
        print("Params", params)
        form = SetLocationForm(
            params or None, instance=request.user.job_seeker
        )
        if form.is_valid():
            form.save()
            percentage(request.user)
            return redirect("analyticsmaven:set-hourly-rate")
        print("Form Error", form.errors)
        return render(request, 'complete-profile.html', {"section": "set-location", "form": form})


@method_decorator(login_required, name='dispatch')
class SetHourlyRate(View):
    def get(self, request):
        return render(request, 'complete-profile.html', {
            "section": "hourly-rate"
        })

    def post(self, request):
        params = request.POST
        print("Parameters", params)
        # return redirect("analyticsmaven:dashboard")
        form = SetHourlyRateForm(
            params or None, instance=request.user.job_seeker
        )
        print("Form is", form)
        if form.is_valid():
            form.save()
            percentage(request.user)
            return redirect("analyticsmaven:dashboard")
        print(form.errors)
        return render(request, 'complete-profile.html', {"section": "hourly-rate", "form": form})



class FavouriteJob(APIView):
    authentication_classes = []

    def post(self, request):
        params = request.POST
        print(request.POST)
        favouritejobs, created = FavouriteJobs.objects.get_or_create(
            user_id=params['user'],
            job_id=params['id']
        )
        favouritejobs.status = True if params['status'] == "true" else False
        favouritejobs.save()
        return JsonResponse({"status": 200})


class MatchedJobList(View):
    def get(self, request):
        matched = JobManagement.objects.filter(
            tools_and_language__in=request.user.job_seeker.tools_and_language.all(), is_active=True).distinct()
        if 'qf' in request.GET:
            matched = matched.filter(
                job_name__icontains=request.GET.get('qf')
            )
        if 'dqf' in request.GET:
            current = date.today()
            if request.GET.get('dqf') == "today":
                matched = matched.filter(
                    created_at__date=current
                )
            elif request.GET.get('dqf') == "yesterday":
                matched = matched.filter(
                    created_at__date=current - timedelta(1)
                )
            elif request.GET.get('dqf') == "week":
                current = current - timedelta(7)
                weekday = current.weekday()
                start_delta = datetime.timedelta(days=weekday)
                start = current - start_delta
                end = start + datetime.timedelta(days=6)
                matched = matched.filter(
                    created_at__date__gte=start,
                    created_at__date__lt=end
                )
            elif request.GET.get('dqf') == "month":
                end = current.replace(day=1)
                end = end - timedelta(days=1)
                start = end.replace(day=1)
                matched = matched.objects.filter(
                    created_at__date__gte=start,
                    created_at__date__lt=end
                )
        if 'tqf' in request.GET:
            print("Time Query Filter", request.GET.get('tqf', None))
        if 'pqf' in request.GET:
            matched = matched.filter(
                credit=request.GET.get('pqf')
            )
        if 'tpqf' in request.GET:
            matched = matched.filter(
                type_of_project=request.GET.get('tpqf')
            )
        if 'mqf' in request.GET:
            matched = matched.filter(
                duration=request.GET.get('mqf')
            )
        if 'eqf' in request.GET:
            pass
            # matched = matched.filter(
            #     experience_level=request.GET.get('eqf')
            # )
        paginator = Paginator(matched, 5)
        page = request.GET.get('page')
        try:
            matched_jobs = paginator.page(page)
        except PageNotAnInteger:
            matched_jobs = paginator.page(1)
        except EmptyPage:
            matched_jobs = paginator.page(paginator.num_pages)
        return render(request, "dashboard.html", {"matching_jobs": matched_jobs, "tab": "1"})


@method_decorator(login_required, name='dispatch')
class FavouriteJobList(View):
    def get(self, request):
        fav = FavouriteJobs.objects.filter(
            user=request.user, status=True
        )
        if 'qf' in request.GET:
            fav = fav.filter(
                user=request.user, status=True, job__job_name__icontains=request.GET.get('qf')
            )
        if 'dqf' in request.GET:
            current = date.today()
            if request.GET.get('dqf') == "today":
                fav = fav.filter(
                    job__created_at__date=current
                )
            elif request.GET.get('dqf') == "yesterday":
                fav = fav.filter(
                    job__created_at__date=current - timedelta(1)
                )
            elif request.GET.get('dqf') == "week":
                current = current - timedelta(7)
                weekday = current.weekday()
                start_delta = datetime.timedelta(days=weekday)
                start = current - start_delta
                end = start + datetime.timedelta(days=6)
                fav = fav.filter(
                    job__created_at__date__gte=start,
                    job__created_at__date__lt=end
                )
            elif request.GET.get('dqf') == "month":
                end = current.replace(day=1)
                end = end - timedelta(days=1)
                start = end.replace(day=1)
                fav = fav.filter(
                    job__created_at__date__gte=start,
                    job__created_at__date__lt=end
                )
        if 'tqf' in request.GET:
            print("Time Query Filter", request.GET.get('tqf', None))
        if 'pqf' in request.GET:
            fav = fav.filter(
                job__credit=request.GET.get('pqf')
            )
        if 'tpqf' in request.GET:
            fav = fav.filter(
                job__type_of_project=request.GET.get('tpqf')
            )
        if 'mqf' in request.GET:
            fav = fav.filter(
                job__duration=request.GET.get('mqf')
            )
        if 'eqf' in request.GET:
            pass
            # fav = fav.filter(
            #     job_experience_level=request.GET.get('eqf')
            # )
        paginator = Paginator(fav, 5)
        page = request.GET.get('page')
        try:
            fav_jobs = paginator.page(page)
        except PageNotAnInteger:
            fav_jobs = paginator.page(1)
        except EmptyPage:
            fav_jobs = paginator.page(paginator.num_pages)
        return render(request, "dashboard.html", {"favourite_jobs": fav_jobs, "tab": "1"})


@method_decorator(login_required, name='dispatch')
class MyJobs(View):
    def get(self, request):
        if request.user.user_type == "Job Seeker":
            applied = request.user.applied_user.filter(status="Applied")
            approved = request.user.applied_user.filter(status="Approved")
            pending = request.user.applied_user.filter(status="Pending")
            closed = request.user.applied_user.filter(status="Closed")
            return render(request, 'myjobs.html', {
                "applied": applied,
                "approved": approved,
                "pending": pending,
                "closed": closed
            })
        else:
            print(request.user)
            # user_comp = Company.objects.filter(
            #     user=request.user)
            # print(user_comp)
            approved = AppliedJobs.objects.filter(status = "Applied",
                job__company_name__user=request.user)
            print(approved)
            # approved = AppliedJobs.objects.filter(
            #     status="Approved", job__company_name__user=request.user)
            # print(approved)
            completed = AppliedJobs.objects.filter(
                Q(status="Completed")| Q(status="Closed"),job__company_name__user=request.user)
            return render(request, 'company-myjobs.html', {
                "approved": approved,
                "completed": completed,
            })

@method_decorator(login_required, name='dispatch')
class JobCompleted(APIView):
    def post(self, request, pk=None):
        job = AppliedJobs.objects.get(id=pk)
        job.status = "Completed"
        job.save()
        send_completed_job_mail(job)
        NotificationList.objects.create(
            sender=request.user,
            receiver=job.job.company_name.user,
            message="{} has mark your {} Job as Completed which you have assigned to him".format(
                request.user.first_name,
                job.job.job_name
            ),
            type="Completed Job",
            link="",
            job=job
        )
        return JsonResponse({"status": 200})

@method_decorator(login_required, name='dispatch')
class JobPending(APIView):
    def post(self, request, pk=None):
        print("Parameters", request.POST)
        job = AppliedJobs.objects.get(id=pk)
        job.status = "Pending"
        job.save()
        JobIncompletedReason.objects.create(
            job_id=pk,
            reason=request.POST['incomplete_reason']
        )
        send_pending_job_mail(job)
        NotificationList.objects.create(
            sender=request.user,
            receiver=job.job.company_name.user,
            message="{} has mark your {} Job as Pending which you have assigned to him".format(
                request.user.first_name,
                job.job.job_name
            ),
            type="Pending Job",
            link="",
            job=job
        )
        return JsonResponse({"status": 200})

@method_decorator(login_required, name='dispatch')
class JobClosed(APIView):
    def post(self, request, pk=None):
        print("Parameters", request.POST)
        job = AppliedJobs.objects.get(id=pk)
        job.status = "Closed"
        job.save()
        review, created = ReviewRating.objects.get_or_create(
            feedback=request.POST['feedback'],
            job=job,
            rate=request.POST['rate'],
            reviewer=request.user,
            reviewee=job.user
        )
        NotificationList.objects.create(
            sender=request.user,
            receiver=job.user,
            message="Congratulations, {} has closed {} Job successfully".format(
                request.user.first_name,
                job.job.job_name
            ),
            type="Closed Job",
            link="",
            job=job
        )
        return JsonResponse({
            "status": 200,
            "user_id": job.user.id,
            "job_id": job.id
        })

@method_decorator(login_required, name='dispatch')
class JobDeclined(APIView):
    def post(self, request, pk=None):
        job = AppliedJobs.objects.get(id=pk)
        job.status = "Decline"
        job.save()
        NotificationList.objects.create(
            sender=request.user,
            receiver=job.user,
            message="{} has revoke/declined {} Job from your bucket".format(
                request.user.first_name,
                job.job.job_name
            ),
            type="Declined Job",
            link="",
            job=job
        )
        return JsonResponse({
            "status": 200,
            "user_id": job.user.id,
            "job_id": job.id
        })


class ReviewCompany(APIView):
    def post(self, request, pk=None):
        job = AppliedJobs.objects.get(id=pk)
        review, created = ReviewRating.objects.get_or_create(
            feedback=request.POST['feedback'],
            job=job,
            rate=request.POST['rate'],
            reviewer=request.user,
            reviewee=job.job.company_name.user
        )
        l = job.job.company_name.user.reviewee.all(
        ).values_list('rate', flat=True)
        avg = reduce(lambda x, y: int(x) + int(y), l) / len(l)
        job.job.company_name.rating = round(avg)
        job.job.company_name.save()
        return JsonResponse({
            "status": 200,
        })


@method_decorator(login_required, name='dispatch')
class Notification(View):
    def get(self, request):
        notification = request.user.notificationreceiver.all()
        # paginator = Paginator(notification, 10)
        # page = request.GET.get('page')
        # try:
        #     notification = paginator.page(page)
        # except PageNotAnInteger:
        #     notification = paginator.page(1)
        # except EmptyPage:
        #     notification = paginator.page(paginator.num_pages)
        return render(request, 'notification.html', {
            "notifications": notification
        })


@method_decorator(login_required, name='dispatch')
class NotificationSeen(APIView):
    def get(self, request):
        request.user.notificationreceiver.all().update(seen=True)
        return JsonResponse({
            "status": 200,
        })

@method_decorator(login_required, name='dispatch')
class JobApproval(View):
    def get(self, request, user=None, applied=None):
        try:
            user = MyUser.objects.get(uuid=user)
            job = AppliedJobs.objects.get(uuid=applied)
            return render(request, 'job_approval.html', {
                "freelancer": user,
                "job": job
            })
        except Exception as e:
            print("Exception as e", e)
            return redirect('analyticsmaven:notification')

@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    def get(self, request, user):
        try:
            user = MyUser.objects.get(uuid=user)
            return render(request, 'job_approval.html', {
                "freelancer": user,
                "job": False
            })
        except Exception as e:
            print("Exception as e", e)
            return redirect('analyticsmaven:notification')


class NotificationRead(View):
    def get(self, request, pk):
        try:
            notification = NotificationList.objects.get(id=pk)
            notification.read = True
            notification.save()
        except Exception as e:
            pass
        if notification.type == "Approved Job":  # Active Jobs
            tab = "tab1"
        elif notification.type == "Applied Job":
            if request.user.user_type == "Job Seeker":
                tab = "tab2"
            else:
                return redirect('analyticsmaven:job-approval', notification.job.user.uuid, notification.job.uuid)
        elif notification.type == "Completed Job":
            tab = "tab2"
        elif notification.type == "Pending Job":
            tab = "tab3"
        elif notification.type == "Closed Job":
            tab = "tab4"
        else:
            tab = "tab1"
        return redirect('/my-jobs?tab={}'.format(tab))


class ApplyJob(View):
    def post(self, request):
        print(request.POST)
        form = ApplyJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()
            send_applied_job_mail(job)
            NotificationList.objects.get_or_create(
                sender=request.user,
                receiver=job.job.company_name.user,
                message="{} has applied for {} Job which you have posted on {} at {}".format(
                    request.user.first_name, job.job.job_name, job.job.created_at.strftime("%d %b %Y"), job.job.created_at.strftime("%I:%M %p")),
                type="Applied Job",
                link="",
                job=job
            )
            return redirect("analyticsmaven:message", job.job.company_name.user.uuid, request.user.uuid, job.job.uuid)
        return redirect("analyticsmaven:dashboard")

############### Job Post Creation URL ###############


class JobPost(View):
    def get(self, request):
        company_percentage(request.user)
        return render(request, 'job_post/post-job-step1.html')

    def post(self, request):
        form = JobPostStep1Form(request.POST)
        if form.is_valid():
            job_post = form.save()
            areaList = []
            if request.POST.getlist('area'):
                for area in request.POST.getlist('area'):
                    try:
                        areaObj = Area.objects.get(id=area)
                    except Exception as e:
                        areaObj, created = Area.objects.get_or_create(
                            name=area.title()
                        )
                        areaObj.is_active = True
                        areaObj.created_by = "USER"
                        areaObj.save()
                    areaList.append(areaObj.id)
                job_post.area = areaList
                job_post.save()
            return redirect(
                "analyticsmaven:job-post-step-2", job_post.uuid
            )
        print(form.errors)
        return render(request, 'job_post/post-job-step1.html')


class EditJobPost(View):
    def get(self, request, uuid=None):
        company_percentage(request.user)
        job_post = JobManagement.objects.get(uuid=uuid)
        return render(request, 'job_post/post-job-step1.html', {"job_post": job_post})

    def post(self, request, uuid=None):
        job_post = JobManagement.objects.get(uuid=uuid)
        form = JobPostStep1Form(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            areaList = []
            if request.POST.getlist('area'):
                for area in request.POST.getlist('area'):
                    try:
                        areaObj = Area.objects.get(id=area)
                    except Exception as e:
                        areaObj, created = Area.objects.get_or_create(
                            name=area.title()
                        )
                        areaObj.is_active = True
                        areaObj.created_by = "USER"
                        areaObj.save()
                    areaList.append(areaObj.id)
                job_post.area = areaList
                job_post.save()
            return redirect(
                "analyticsmaven:job-post-step-2", job_post.uuid
            )

        print(form.errors)
        return render(request, 'job_post/post-job-step1.html')


class JobPostStep2(View):
    def get(self, request, uuid=None):
        company_percentage(request.user)
        job = JobManagement.objects.get(uuid=uuid)
        return render(request, 'job_post/post-job-step2.html', {"job": job})

    def post(self, request, uuid=None):
        job_post = JobManagement.objects.get(uuid=uuid)
        form = JobPostStep2Form(request.POST or None, instance=job_post)
        if form.is_valid():
            form.save()
            if request.POST.getlist('tools_and_language'):
                print(request.POST.getlist('tools_and_language'))
                skillList = []
                for skill in request.POST.getlist('tools_and_language'):
                    try:
                        skillObj = Skills.objects.get(id=skill)
                    except Exception as e:
                        skillObj, created = Skills.objects.get_or_create(
                            name=skill.title()
                        )
                        skillObj.is_active = True
                        skillObj.created_by = "USER"
                        skillObj.save()
                    skillList.append(skillObj.id)
                job_post.tools_and_language = skillList
                job_post.save()
            return redirect(
                "analyticsmaven:job-post-step-3", job_post.uuid
            )
        return render(request, 'job_post/post-job-step2.html', {"job": job_post, "form": form})


class JobPostStep3(View):
    def get(self, request, uuid=None):
        company_percentage(request.user)
        job = JobManagement.objects.get(uuid=uuid)
        return render(request, 'job_post/post-job-step3.html', {"job": job})

    def post(self, request, uuid=None):
        params = request.POST
        job_post = JobManagement.objects.get(uuid=uuid)
        form = JobPostStep3Form(request.POST, instance=job_post)
        print("params", params)
        if form.is_valid():
            form.save()
            if "language" in params and request.POST.getlist('language'):
                languageList = []
                for language in request.POST.getlist('language'):
                    try:
                        languageObj = Language.objects.get(id=language)
                    except Exception as e:
                        print("Lanuage", language)
                        languageObj, created = Language.objects.get_or_create(
                            language=language.title()
                        )
                        languageObj.is_active = True
                        languageObj.created_by = "USER"
                        languageObj.save()
                    languageList.append(languageObj.id)
                job_post.language = languageList
            if "country" in params and request.POST.getlist('country'):
                countryList = []
                for country in request.POST.getlist('country'):
                    try:
                        countryObj = Country.objects.get(id=country)
                    except Exception as e:
                        countryObj, created = Country.objects.get_or_create(
                            name=country.title()
                        )
                        countryObj.is_active = True
                        countryObj.created_by = "USER"
                        countryObj.save()
                    countryList.append(countryObj.id)
                job_post.country = countryList
            job_post.save()
            return redirect(
                "analyticsmaven:job-post-step-4", job_post.uuid
            )
        print(form.errors)
        return render(request, 'job_post/post-job-step3.html', {"form": form, "job": job_post})


class JobPostStep4(View):
    def get(self, request, uuid=None):
        company_percentage(request.user)
        job = JobManagement.objects.get(uuid=uuid)
        return render(request, 'job_post/post-job-step4.html', {"job": job})

    def post(self, request, uuid=None):
        job = JobManagement.objects.get(uuid=uuid)
        form = JobPostStep4Form(request.POST, instance=job)
        if form.is_valid():
            form.save()
            post_job_successfully_mail(job)
            return render(request, 'job_post/post-job-step4.html', {"job": job,"popup": True})
            # return redirect('analyticsmaven:dashboard')
        print("Forms Errors:--",form.errors)
        return render(request, 'job_post/post-job-step4.html', {"job": job})

############### Company Profile Management URL ###############


class ViewJobSeeker(View):
    def get(self, request, uuid=None):
        user = MyUser.objects.get(uuid=uuid)
        return render(request, 'jobs2.html', {"user": user})


class ViewApplicants(View):
    def get(self, request, uuid=None):
        job = JobManagement.objects.get(uuid=uuid)
        job_applicants = AppliedJobs.objects.filter(job__job_name=job.job_name)
        company = JobManagement.objects.filter(
            company_name__company_name=request.user.first_name)
        print("job", job)
        print("job_applicants", job_applicants)
        print("company", company)
        paginator = Paginator(company, 3)
        if 'pages' in request.GET:
            page = request.GET.get('pages')
            tab = "tab2"
        else:
            page = request.GET.get('page')
            tab = "tab1"
        try:
            companypage = paginator.page(page)
        except PageNotAnInteger:
            companypage = paginator.page(1)
        except EmptyPage:
            companypage = paginator.page(paginator.num_pages)
        company_percentage(request.user)
        return render(request, 'jobs.html', {"job_seeker": job_applicants, "companypage": companypage, })


class CompanyProfile(View):
    def get(self, request):
        company = Company.objects.get(email=request.user)
        posted_jobs = JobManagement.objects.filter(
                company_name__company_name=request.user.first_name)
        return render(request, 'company-profile.html',{'company':company,'posted_jobs':posted_jobs, "company_profile":True})
############### Posted Job View URL ##############


class ViewPostedJobs(View):
    def get(self, request, uuid=None):
        job = JobManagement.objects.get(uuid=uuid)

        job_seeker = JobSeeker.objects.filter(
            user__is_active=True,
            tools_and_language__in=request.user.company.company_name_jobmanagement.values_list(
                'tools_and_language', flat=True)
        ).exclude(user__is_superuser=True)
        return render(request, 'posted-job-view.html', {"job": job, "job_seeker": job_seeker})

class JobsDetail(View):
    def get(self, request, uuid=None):
        job = JobManagement.objects.get(uuid=uuid)
        return render(request, 'job-detail.html', {"job": job})



class DeletePostedJobs(APIView):
    def get(self, request, uuid=None):
        job = JobManagement.objects.get(uuid=uuid)
        job.delete()
        delete_job_successfully_mail(job)
        return JsonResponse({"status": 200})


############### Static Moanagment URL ###############


class AboutUsView(View):
    '''About Us-Website'''

    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        # about = AboutUs.objects.first()
        member = BoardMember.objects.all()
        about = AboutUs.objects.all()
        return render(request, "static_pages/about-us.html", {
            "template_name": template,
            "about": about,
            "member": member
        })


class Faq(View):
    '''FAQ-Website'''

    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        question = FAQ.objects.all()
        if 'tag' in request.GET:
            question = question.filter(tagging__name__icontains=request.GET.get('tag').strip())
        page = request.GET.get('page')
        paginator = Paginator(question, 10)
        try:
            question = paginator.page(page)
        except PageNotAnInteger:
            question = paginator.page(1)
        except EmptyPage:
            question = paginator.page(paginator.num_pages)
        return render(request, "static_pages/faq.html", {
            "template_name": template,
            "question": question
        })


class PrivacyPolicyView(View):
    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        privacy = PrivacyPolicy.objects.get()
        return render(request, "static_pages/privacy-policy.html", {"template_name": template,'privacy':privacy})


class Terms(View):
    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        try:
            terms = TermsAndConditions.objects.get()
            return render(request, "static_pages/terms.html", {
                "template_name": template, "terms": terms
            })
        except:
            return render(request, "static_pages/terms.html", {
                "template_name": template, "terms": {}
            })

############ Admin Forgot Password View ###############


class ForgotPassword(View):
    '''View for Forgot Password for Admin'''

    def get(self, request):
        return redirect('/admin/password_reset/')

    def post(self, request):
        try:
            try:
                useremail = request.POST.get('email')
                user = MyUser.objects.get(email=useremail)
            except:
                messages.success(request, ('Email id not registered.'))
                return redirect('/admin/password_reset/')
            if user.is_superuser:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                pre_link = 'https://' if request.is_secure() else 'http://'
                link = pre_link+str(get_current_site(request)) + \
                    "/forgot-password/{}".format(uid.decode('utf8'))
                user.send_forgot_mail(link)
                return render(request, 'admin/password_reset_sent.html', context={"message": "Password reset link is sent to your email address."})
            messages.success(
                request, ('Email id not Authorised to use this functionality.'))
            return redirect('/admin/password_reset/')

        except Exception as e:
            print(e)
            error = "Sorry! Something went wrong, we can't send reset link."
            return render(request, 'admin/password_reset_sent.html', {'error': error})


class ResetPassword(View):
    '''View for Reset Password for Admin'''

    def get(self, request, uidb64=None):
        return render(request, 'admin/resetpassword.html', {'uids': uidb64})

    def post(self, request, uidb64=None):
        newpassword = request.POST['newpassword']
        confirm_password = request.POST['confirm_password']
        uid = force_text(urlsafe_base64_decode(uidb64))
        if (newpassword == confirm_password):
            try:
                user = JobSeeker.objects.get(pk=uid)
            except:
                error = "Sorry! Something went wrong, we can't reset your password."
                return render(request, 'admin/password_reset_sent.html', {'error': error})
            user.set_password(newpassword)
            user.save()
            messages.success(
                request, ('Password Changed Successfully.'))
            return redirect('/admin/')
        else:
            return render(request, 'admin/resetpassword.html', {'uids': uidb64, 'message': 'Password and Confirm password does not match.'})


####################### Chat URL ##########################
class Message(View):
    '''View for Chat'''

    def get(self, request, company=None, jobseeker=None, job=None):
        try:
            company = MyUser.objects.get(uuid=company)
            jobseeker = MyUser.objects.get(uuid=jobseeker)
            job = JobManagement.objects.get(uuid=job)
            chatobj, created = ChatList.objects.get_or_create(
                company=company,
                jobseeker=jobseeker,
                job=job,
            )
            chatobj.chatlist.filter(read=False).update(read=True)
            if not Chats.objects.filter(chat=chatobj).count():
                try:
                    message = AppliedJobs.objects.get(user=request.user,job=job).reason
                    print("Message",message)
                except Exception as e:
                    print("Exception as e during first Chat creation",e)
                    message = "Invitation Send untill he has not accept your Invitation you can't Message them"
                Chats.objects.create(
                    sender=request.user,
                    receiver=jobseeker if request.user.user_type == "Company" else company,
                    chat=chatobj,
                    message= message,
                    msg_type="invitation",
                    read=False
                )
            if request.user.user_type == "Company":
                chatobj.companydeleted = False
            else:
                chatobj.jobseekerdeleted = False
            chatobj.save()
            if request.user.user_type == "Company":
                chat_list = request.user.company_chat.filter(
                    companydeleted=False
                )
            else:
                chat_list = request.user.jobseeker_chat.filter(
                    jobseekerdeleted=False
                )
            if 'chatqf' in request.GET:
                chat_list = chat_list.filter(Q(
                    job__job_name__icontains=request.GET.get("chatqf")
                ) | Q(
                    company__first_name__icontains=request.GET.get("chatqf")
                ) | Q(
                    jobseeker__first_name__icontains=request.GET.get("chatqf")
                ))
        except Exception as e:
            print("Exception as  company", e)
        return render(request, 'message.html', {
            'type': 'message',
            'chat': chatobj,
            'chatid': chatobj.id,
            "receiver": company if request.user.user_type == "Job Seeker" else jobseeker,
            "chat_data": chatobj.chatlist.filter(deleted=False),
            "chat_list": chat_list,
        })


class MessageRedirect(View):
    '''View for Chat'''

    def get(self, request):
        obj = Chats.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)).latest('created_at')
        return redirect("analyticsmaven:message", obj.chat.company.uuid, obj.chat.jobseeker.uuid, obj.chat.job.uuid)


class DeleteChatMessage(APIView):
    '''View for Chat'''

    def post(self, request):
        params = request.POST
        try:
            chat = Chats.objects.get(id=params['message'])
            chat.deleted = True
            chat.save()
        except Exception as e:
            print("Exception as e", e)
        return JsonResponse({"status": 200})


class DeleteChatList(APIView):
    '''View for Chat'''

    def post(self, request):
        params = request.POST
        print("User Type", request.user.user_type)
        try:
            chat = ChatList.objects.get(id=params['chatlist'])
            if request.user.user_type == "Company":
                chat.companydeleted = True
            else:
                chat.jobseekerdeleted = True
            chat.save()
        except Exception as e:
            print("Exception as e", e)
        return JsonResponse({"status": 200})


class InvitationAccept(View):

    '''View for Chat'''

    def post(self, request, pk):
        params = request.POST
        try:
            obj = ChatList.objects.get(id=pk)
            obj.invitation = True
            obj.save()
            chat_message = obj.chatlist.first()
            chat_message.message = "Let's Chat."
            chat_message.msg_type = 'text'
            chat_message.save()
        except Exception as e:
            print("Exception as e", e)
        return redirect("analyticsmaven:message", obj.company.uuid, obj.jobseeker.uuid, obj.job.uuid)


class JobSeekerSearch(View):

    def get(self, request):
        jobs = JobManagement.objects.filter(is_active=True)
        if request.GET.get('content'):
            jobs = jobs.filter(
                Q(job_name__icontains=request.GET.get('content')) |
                Q(company_name__company_name__icontains=request.GET.get('content')) |
                Q(type_of_project__icontains=request.GET.get('content')) |
                Q(duration__icontains=request.GET.get('content'))
            )
        if request.GET.get('skill'):
            jobs = jobs.filter(
                Q(tools_and_language__in=request.GET.get('skill').split(','))
            )
        if request.GET.get('location'):
            jobs = jobs.filter(
                Q(country__in=request.GET.get('location').split(','))
            )
        paginator = Paginator(jobs, 5)
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
        return render(request, "employee-search.html", {
            "jobs": jobs,
            "content": request.GET.get('content')
        })


class CompanySearch(View):
    def get(self, request):
        job_seeker = MyUser.objects.filter(
            Q(first_name__icontains=request.GET.get('content')) | Q(last_name__icontains=request.GET.get('content')) ,
            user_type='Job Seeker',
        )
        if request.GET.get('skill'):
            job_seeker = job_seeker.filter(
                Q(job_seeker__tools_and_language__in=request.GET.get('skill').split(','))
            )
            # return HttpResponse(job_seeker)
        if request.GET.get('location'):
            # return HttpResponse(request.GET.get('location'))
            
            job_seeker = job_seeker.filter(
                Q(job_seeker__country__in=request.GET.get('location').split(','))
            )
            # return HttpResponse(job_seeker)
        paginator = Paginator(job_seeker, 5)
        page = request.GET.get('page')
        try:
            job_seeker = paginator.page(page)
        except PageNotAnInteger:
            job_seeker = paginator.page(1)
        except EmptyPage:
            job_seeker = paginator.page(paginator.num_pages)
        return render(request, 'company-search.html', {"job_seeker": job_seeker, "content": request.GET.get('content')})


class CompanyDashboard(View):
    def get(self, request):
        tab = "tab1"
        company = JobManagement.objects.filter(
            company_name__company_name=request.user.first_name)
        print(company)
        paginator = Paginator(company, 3)
        if 'pages' in request.GET:
            page = request.GET.get('pages')
            tab = "tab2"
        else:
            page = request.GET.get('page')
            tab = "tab1"
        try:
            companypage = paginator.page(page)
        except PageNotAnInteger:
            companypage = paginator.page(1)
        except EmptyPage:
            companypage = paginator.page(paginator.num_pages)
        company_percentage(request.user)
        seeker = AppliedJobs.objects.filter(
            job__company_name=request.user.company
        ).order_by('user').distinct('user')
        # job_seeker = JobSeeker.objects.filter(
        #     user__is_active=True,
        #     tools_and_language__in=request.user.company.company_name_jobmanagement.values_list(
        #         'tools_and_language', flat=True)
        # ).exclude(user__is_superuser=True)
        paginator = Paginator(seeker, 5)
        page = request.GET.get('page')
        try:
            job_seeker = paginator.page(page)
        except PageNotAnInteger:
            job_seeker = paginator.page(1)
        except EmptyPage:
            job_seeker = paginator.page(paginator.num_pages)
        return render(request, 'jobs.html', {"job_seeker": job_seeker, "companypage": companypage, "tab": tab})


class CompanyDashboardFilter(View):
    def post(self, request):
        params = (request.POST)
        print("params", params)
        applied_user = AppliedJobs.objects.filter(
            job__company_name__company_name=request.user.first_name)
        print("Applied User", applied_user)
        if 'credit' in params:
            applied_user = applied_user.filter(
                job__credit__icontains=params['credit'])
        if "type_of_project" in params:
            applied_user = applied_user.filter(
                job__type_of_project__icontains=params['type_of_project'])
        if "duration" in params:
            applied_user = applied_user.filter(
                job__duration__icontains=params['duration'])
        print(applied_user)
        paginator = Paginator(applied_user, 6)
        page = request.GET.get('page')
        try:
            applied_user = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            applied_user = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            applied_user = paginator.page(paginator.num_pages)
        return render(request, "jobs.html", {"tab": "0", "job_seeker": applied_user})


class ContactUs(View):
    '''Contact Us-Website'''

    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        return render(request, "static_pages/contact-us.html", {"template_name": template})

    def post(self, request):
        form = ContactUsForm(request.POST)
        if request.user:
            template = 'dashboardheader.html'
        else:
            template = 'base.html'
        if form.is_valid():
            form.save()
            message = "We will contact you shortlty"
            return render(request, 'static_pages/contact-us.html', {
                "message": message,
                "template_name": template,
                "popup": True
            })
        return render(request, 'static_pages/contact-us.html')


class Career(View):
    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        profession = Profession.objects.all()
        return render(request, "static_pages/career.html", {
            "template_name": template,
            "profession_list": profession
        })

    def post(self, request):
        print(request.POST)
        profession = Profession.objects.all()
        form = CareerForm(request.POST, request.FILES)
        if request.user:
            template = 'dashboardheader.html'
        else:
            template = 'base.html'
        if form.is_valid():
            carrerObj = form.save(commit=False)
            carrerObj.profession_id = request.POST['profession']
            carrerObj.save()
            message = "Your interest has been recorded successfully."
            return render(request, "static_pages/career.html", {
                "template_name": template,
                "profession_list": profession,
                "popup": True
            })
        print('Errors', form.errors)
        return render(request, 'static_pages/career.html', {
            "form": form,
            "template_name": template,
            'profession_list': profession
        })

# Payment Management


class AdvancePayment(View):
    def post(self, request):
        params = request.POST
        print("Parameters", params)
        response = payment(
            request, params['job'], params['advance'], "Advance")
        return redirect(response['url'])


class PaypalPaymentAdvance(View):
    def get(self, request, pk=None):
        transaction = TransactionManagement.objects.filter(
            sender=request.user
        ).latest('created_at')
        transaction_details = ast.literal_eval(
            paypal_transaction_details(transaction.key).decode("utf-8")
        )
        if transaction_details['status'] == 'COMPLETED':
            transaction.status = "COMPLETED"
            transaction.save()
        return redirect('analyticsmaven:my-jobs')

    def post(self, request, pk=None):
        transaction = TransactionManagement.objects.filter(
            sender=request.user).latest('created_at')
        transaction_details = ast.literal_eval(
            paypal_transaction_details(transaction.key).decode("utf-8"))
        if transaction_details['status'] == 'COMPLETED':
            transaction.status = "COMPLETED"
            transaction.save()
        return redirect('analyticsmaven:my-jobs')


class JobApproved(View):
    def post(self, request):
        params = request.POST
        print("Params", params)
        response = payment(request, params['job'], params['escrow'], "Escrow")
        return redirect(response['url'])


class PaypalPaymentEscrow(View):
    def get(self, request, pk=None):
        transaction = TransactionManagement.objects.filter(
            sender=request.user
        ).latest('created_at')
        transaction_details = ast.literal_eval(
            paypal_transaction_details(transaction.key).decode("utf-8")
        )
        if transaction_details['status'] == 'COMPLETED':
            transaction.status = "COMPLETED"
            transaction.save()
            job = AppliedJobs.objects.get(id=pk)
            job.status = "Approved"
            job.save()
            NotificationList.objects.create(
                sender=request.user,
                receiver=job.user,
                message="Congratulations, {} has awarded {} Job to you".format(
                    request.user.first_name,
                    job.job.job_name
                ),
                type="Approved Job",
                link="",
                job=job
            )
        return redirect('analyticsmaven:dashboard')

    def post(self, request, pk=None):
        transaction = TransactionManagement.objects.filter(
            sender=request.user).latest('created_at')
        transaction_details = ast.literal_eval(
            paypal_transaction_details(transaction.key).decode("utf-8"))
        if transaction_details['status'] == 'COMPLETED':
            transaction.status = "COMPLETED"
            transaction.save()
            ob = AppliedJobs.objects.get(id=pk)
            job.status = "Approved"
            job.save()
            NotificationList.objects.create(
                sender=request.user,
                receiver=job.user,
                message="Congratulations, {} has awarded {} Job to you".format(
                    request.user.first_name,
                    job.job.job_name
                ),
                type="Approved Job",
                link="",
                job=job
            )
        return redirect('analyticsmaven:dashboard')


class TopSkills(View):
    def get(self, request):
        if request.user:
            template = 'base.html'
        else:
            template = 'base.html'
        skill_list = Skills.objects.filter(
            name__icontains=request.GET.get('skill')).values_list('id', flat=True)
        job_seeker = JobSeeker.objects.filter(
            user__is_active=True, tools_and_language__in=skill_list)
        jobs = JobManagement.objects.filter(
            is_active=True, tools_and_language__in=skill_list)
        return render(request, "top-skills.html", {
            "template_name": template,
            "job_seeker": job_seeker,
            "jobs": jobs,
            'blank': True if not job_seeker.count() and not jobs.count() else False
        })



class TopSkillsAction(View):
    def get(self, request):
        if request.user.id:
            return redirect("analyticsmaven:dashboard")
        return redirect("analyticsmaven:login")


class ReleasePayment(View):
    def get(self, request, pk=None):
        transaction = TransactionManagement.objects.get(id=pk)
        # adminrelease(transaction)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ReferFriendView(View):
    def post(self, request):
        params = request.POST
        ReferFriend.objects.create(user=request.user,email=params['email'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"?refer=true")