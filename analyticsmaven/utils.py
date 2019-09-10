from .models import UserSkillRate, MyUser


def user_experience_level(request, params):
    try:
        user = MyUser.objects.get(id=params['user'])
        print("User", user)
    except Exception as e:
        return
    rate = 0
    for skill in user.job_seeker.tools_and_language.all():
        try:
            value = UserSkillRate.objects.get(
                user=user,
                skill_id=skill
            ).rate
        except Exception as e:
            print("Exception as e", e)
            value = 0
        rate += int(value)
    print("Total Rate", rate)
    rating = int(rate/user.job_seeker.tools_and_language.count())
    print("Average Rating", rating)
    if int(rating) == 5 or int(rating) == 4:
        user.job_seeker.experience_level = 'Expert'
    elif int(rating) == 3:
        user.job_seeker.experience_level = 'Intermediate'
    else:
        user.job_seeker.experience_level = 'Beginner'
    user.job_seeker.save()
    print("Experience", user.job_seeker.experience_level)
