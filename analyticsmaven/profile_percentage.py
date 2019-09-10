def percentage(user):
    try:
        status = 0
        profile = {
            "first_name": 10,
            "avatar":5,
            "area": 5,
            "industry": 5,
            "tools_and_language": 5,
            "tools_and_language_rating": 5,
            "education_details": 5,
            "employment_detials": 5,
            "experience_level": 5,
            "professional_title": 5,
            "overview": 5,
            "language_known": 5,
            "language_rating": 5,
            "avialiblity": 5,
            "city": 5,
            "postal_code": 5,
            "phone_no": 5,
            "country": 5,
            "timezone": 5
        }
        if user.job_seeker.first_name:
            # print('First Name', profile['first_name'])
            status += profile['first_name']
        if user.avatar:
            # print('First Name', profile['first_name'])
            status += profile['avatar']
        if user.job_seeker.area.count():
            # print('Area', profile['area'])
            status += profile['area']
        if user.job_seeker.industry.count():
            # print('Industry', profile['industry'])
            status += profile['industry']
        if user.job_seeker.tools_and_language.count():
            # print('Tools and Language', profile['tools_and_language'])
            status += profile['tools_and_language']
        if user.job_seeker.job_seeker_education.count():
            # print('Education Details', profile['education_details'])
            status += profile['education_details']
        if user.job_seeker.job_seeker_employment.count():
            # print('Employment Details', profile['employment_detials'])
            status += profile['employment_detials']
        if user.user_skill.count():
            # print('Skill Rating', profile['tools_and_language_rating'])
            status += profile['tools_and_language_rating']
        if user.job_seeker.experience_level:
            # print('Experience', profile['experience_level'])
            status += profile['experience_level']
        if user.job_seeker.professional_title:
            # print('Title', profile['professional_title'])
            status += profile['professional_title']
        if user.job_seeker.overview:
            # print('Overview', profile['overview'])
            status += profile['overview']
        if user.job_seeker.language_known.count():
            # print('Language', profile['language_known'])
            status += profile['language_known']
        if user.user_language.count():
            # print('Language Rating', profile['language_rating'])
            status += profile['language_rating']
        if user.job_seeker.week_availability:
            # print('Availibility', profile['avialiblity'])
            status += profile['avialiblity']
        if user.job_seeker.city:
            # print('City', profile['city'])
            status += profile['city']
        if user.job_seeker.postal_code:
            # print('Postal Code', profile['postal_code'])
            status += profile['postal_code']
        if user.job_seeker.phone_no:
            # print('Phone Number', profile['phone_no'])
            status += profile['phone_no']
        if user.job_seeker.country:
            # print('Country', profile['country'])
            status += profile['country']
        if user.job_seeker.timezone:
            # print('Time Zone', profile['timezone'])
            status += profile['timezone']
        print('Total percentage', status)
        user.job_seeker.profile_completion = status
        user.job_seeker.save()
        return
    except:
        return
