from .views import *
import logging
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate
from .models import *


def social(strategy,  request, *args, **kwargs):
    print("Details", kwargs['details'])
    user_type = strategy.session_get('user_type', 'Job Seeker')
    print("User Type", user_type)
    if not user_type:
        # return redirect('/login')
        return render(request, "index.html", {"type": "login", "login_failed_message": "We are not able to recoginsed your User Type please prefer sign up rather sign in for this"})
    user, created = MyUser.objects.get_or_create(
        email=kwargs['details']['email'],
    )
    if user.is_active:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/dashboard')
    try:
        user.sign_up = user.social_auth.latest('id').provider
    except Exception as e:
        print("Excetion as e", e)
    # user.user_type = user_type
    user.first_name = kwargs['details']['first_name']
    user.last_name = kwargs['details']['last_name']
    if user_type == "Job Seeker":
        try:
            jobseeker, created = JobSeeker.objects.get_or_create(
                user=user
            )
        except Exception as e:
            return render(request, "index.html", {"type": "login", "message": "Your Social Account is already registered with us but it seems you have not activated your Account.Please, activate it and then login."})
        user.user_type = "Job Seeker"
        user.save()
        jobseeker.email = user.email
        jobseeker.first_name = user.first_name
        jobseeker.last_name = user.last_name
        try:
            user.social_auth.get(provider='linkedin-oauth2')
            extra_data = user.social_auth.get(
                provider='linkedin-oauth2').extra_data
            jobseeker.professional_title = extra_data['headline'] if 'headline' in extra_data else None
            jobseeker.overview = extra_data['summary'] if 'summary' in extra_data else ''
            if 'positions' in extra_data:
                if extra_data['positions']['values']:
                    for emp in extra_data['positions']['values']:
                        Employment.objects.get_or_create(
                            seeker=jobseeker,
                            title=emp['title'] if 'title' in emp else None,
                            company=emp['company']['name'] if 'company' in emp and emp['company']['name'] else None,
                            location=emp['location']['name'] if 'location' in emp and emp['location'] else extra_data['location']['name'],
                            currently=True if emp['isCurrent'] else False,
                            from_month=emp['startDate']['month'] if 'startDate' in emp else None,
                            from_year=emp['startDate']['year'] if 'startDate' in emp else None,
                            to_month=emp['endDate']['month'] if 'endDate' in emp else "1",
                            to_year=emp['endDate']['year'] if 'endDate' in emp else "",
                            description=emp['summary'] if 'summary' in emp else ""
                        )
        except Exception as e:
            print("Exception as e", e)
        jobseeker.save()
        return HttpResponseRedirect('/registration-details/%s' % user.uuid)
    else:
        try:
            company, created = Company.objects.get_or_create(
                user=user
            )
        except Exception as e:
            return render(request, "index.html", {"type": "login", "message": "Email already registered, you can login to your account."})
        user.user_type = "Company"
        user.save()
        company.email = user.email
        company.company_name = user.first_name
        company.save()
        return HttpResponseRedirect('/company-registration/%s' % user.uuid)
