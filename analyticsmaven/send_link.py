
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from bluerobins.settings import os
from templated_email import send_templated_mail


def send_link(request, user):
    """Method to send reset password link on email"""
    pre_link = 'https://' if os.environ.get("HTTPS") == "on" else 'http://'
    link = pre_link+str(get_current_site(request)) + \
        "/forgot/{}".format(user.uuid)
    print("Sending link", link)
    send_templated_mail(
        template_name='user_management/forgot_password_user.email',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        context={
            "first": user.first_name,
            "last": user.last_name if user.last_name else '',
            "link": link,
            "message": "By Clicking the below button you can Reset your Account Password."
        },
    )
    return True


def send_mail(request, user):
    try:
        pre_link = 'https://' if os.environ.get("HTTPS") == "on" else 'http://'
        print("Pre Link", pre_link)
        link = pre_link+str(get_current_site(request)) + \
            "/activate-your-account/{}".format(user.uuid)
        print("Sending link", link)
        send_templated_mail(
            template_name='user_management/active.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            context={
                "first": user.first_name,
                "last": user.last_name if user.last_name else '',
                "link": link,
                "message": "By Clicking the below button you can Activate your Account"
            },
        )
    except Exception as e:
        print("Exception as e", e)


def send_applied_job_mail(job):
    try:
        send_templated_mail(
            template_name='job/applied_job.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job.user.email],
            context={
                "username": job.user.first_name,
                "message": "You have applied for {} Job posted by {} Company.Thanks for your interest.".format(
                    job.job.job_name,
                    job.job.company_name.company_name
                )
            },
        )

        send_templated_mail(
            template_name='job/applied_job_company.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job.job.company_name.user.email],
            context={
                "username": job.job.company_name,
                "message": "{} have applied fon your {} Job".format(
                    job.user.first_name,
                    job.job.job_name
                )
            },
        )
    except Exception as e:
        print("Exception as e", e)


def send_completed_job_mail(job):
    try:
        send_templated_mail(
            template_name='job/completed_job.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job.job.company_name.user.email],
            context={
                "username": job.job.company_name.company_name,
                "message": "{} have marked your {} Job as Completed which you have posted on {}.Thanks for your interest.".format(job.user.first_name, job.job.job_name, job.job.created_at)
            },
        )
    except Exception as e:
        print("Exception as e", e)


def send_pending_job_mail(job):
    try:
        send_templated_mail(
            template_name='job/pending_job.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job.user.email],
            context={
                "username": job.user.first_name,
                "message": "{} have marked this {} Job as Pending which you have marked as Complted.".format(job.job.company_name.company_name, job.job.job_name)
            },
        )
    except Exception as e:
        print("Exception as e", e)


def post_job_successfully_mail(job):
    try:
        send_templated_mail(
            template_name='company/job.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job.company_name.user.email],
            context={
                "username": job.company_name.user.first_name,
                "message": "Your job is posted Successfully",
                "subject": "Post Job"
            },
        )
    except Exception as e:
        print("Exception as e", e)


def delete_job_successfully_mail(job):
    try:
        send_templated_mail(
            template_name='company/job.email',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job.company_name.user.email],
            context={
                "username": job.company_name.user.first_name,
                "message": "Your Job is deleted Successfully",
                "subject": "Delete Job"
            },
        )
    except Exception as e:
        print("Exception as e", e)
