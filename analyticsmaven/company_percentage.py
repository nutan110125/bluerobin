def company_percentage(user):
    status = 0
    profile = {
        "company_name": 34,
        "industry": 34,
        "avatar": 32,

    }
    if user.company.company_name:
        # print('First Name', profile['company_name'])
        status += profile['company_name']
    if user.company.industry.count():
        # print('Tools and Language', profile['tools_and_language'])
        status += profile['industry']
    if user.avatar:
        # print('Tools and Language', profile['tools_and_language'])
        status += profile['avatar']
    print('Total percentage', status)
    user.company.profile_completion = status
    user.company.save()
    return
