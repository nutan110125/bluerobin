import datetime
from .models import *
from staticmanagement.models import *

def admin_data(request):
    """Method for retrieving data for admin """
    jobseekers = JobSeeker.objects.all()
    company = Company.objects.all()
    total_jobs = JobManagement.objects.all()
    active_jobs = JobManagement.objects.filter(is_active=True)
    work = HowitWorks.objects.all()
    who = WhoAreWe.objects.last()
    return {"count_jobseekers": len(jobseekers), "jobseekers":jobseekers, "count_company": len(company), "companies":company, "count_total_jobs": len(total_jobs), "count_active_jobs": len(active_jobs),"work":work,"who":who}


def skillSet(request):
    skills = Skills.objects.all().exclude(name__isnull=True).exclude(name='')
    industrys = Industry.objects.all().exclude(name__isnull=True).exclude(name='')
    areas = Area.objects.filter(is_active = True).exclude(name__isnull=True).exclude(name='')
    languages = Language.objects.all().exclude(language__isnull=True).exclude(language='')
    country = Country.objects.all().exclude(name__isnull=True).exclude(name='')
    timezone = Timezone.objects.all().exclude(name__isnull=True).exclude(name='')
    hours = Hours.objects.all()
    return {
        "skills": skills,
        "industries": industrys,
        "areas": areas,
        "languages": languages,
        "country": country,
        "timezone": timezone,
        "hours": hours
    }


def notification(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return {
            "ncount": request.user.notificationreceiver.filter(seen=False).count(),
            "unread": request.user.chatreceiver.filter(read=False).count()
        }
    return {
        "ncount": None,
        "unread": None
    }


def year_list(request):
    yearList = []
    current_year = datetime.datetime.now().date().year
    for i in range(current_year, 1950, -1):
        yearList.append(i)
    return {"year_list": yearList}


def latestjob(request):
    latest_jobs = JobManagement.objects.all()[:5]
    return {"latest_jobs": latest_jobs}


def favjobs(request):
    if request.user.id and request.user.user_type == 'Job Seeker':
        jobs = request.user.favourite_job_user.filter(
            status=True)
        favlist = jobs.values_list('job__id', flat=True)
        return {"fav": favlist}
    return []


def appliedjobs(request):
    if request.user.id and request.user.user_type == 'Job Seeker':
        jobs = request.user.applied_user.filter(
            status="Applied"
        )
        appliedlist = jobs.values_list('job__id', flat=True)
        
        return {"applied": appliedlist}
    return []


def hourlyrate(request):
    analytics_rate = AnalyticsRate.objects.first()
    return {"analytics_rate": analytics_rate}


def user_experience_level(request):
    if not request.user.is_superuser and request.user.id and request.user.user_type == "Job Seeker":
        rate = 0
        for skill in request.user.job_seeker.tools_and_language.all():
            try:
                value = UserSkillRate.objects.get(
                    user=request.user,
                    skill_id=skill
                ).rate
            except Exception as e:
                print("Exception as e", e)
                value = 0
            rate += int(value)
        print("Total Rate", rate)
        rating = int(rate/request.user.job_seeker.tools_and_language.count())
        print("Average Rating", rating)
        if int(rating) == 5 or int(rating) == 4:
            request.user.job_seeker.experience_level = 'Expert'
        elif int(rating) == 3:
            request.user.job_seeker.experience_level = 'Intermediate'
        else:
            request.user.job_seeker.experience_level = 'Beginner'
        request.user.job_seeker.save()
        print("Experience", request.user.job_seeker.experience_level)
    return {"level": ""}
