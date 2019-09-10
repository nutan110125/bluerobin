import datetime
from dateutil.relativedelta import relativedelta
from django import template
from django.db.models import Avg
register = template.Library()


from analyticsmaven.models import UserSkillRate


@register.filter
def skill_filter(user):
    return UserSkillRate.objects.filter(user=user).exclude(rate=0).order_by('rate')


@register.filter
def current_duration(input):
    current = datetime.datetime.now()
    if not input:
        return input
    input = input.replace(tzinfo=None)
    duration = current - input
    if duration.days <= 1:
        if duration.seconds // 3600 >= 1:
            return str(duration.seconds // 3600) + " hours ago"
        return str(int(duration.seconds % 3600 / 60.0)) + " minutes ago"
    elif duration.days == 1:
        return "Yesterday"
    else:
        return input.strftime("%d/%m/%y")


@register.filter
def language_rate(input, pk):
    rating = input.get(language_id=pk)
    return rating.rate


@register.filter
def unread_count(input, user):
    return input.chatlist.filter(receiver=user, read=False).count()


@register.filter
def applied(input, user):
    try:
        user.applied_user.get(job=input)
        print("True")
        return True
    except Exception as e:
        print("Exception as e", e)
        return False


@register.filter
def rating_status(input, pk):
    try:
        rating = input.get(language_id=pk).rate
    except:
        rating = 0
    if int(rating) == 5:
        return '(Mother tongue / Fluent)'
    if int(rating) == 4:
        return '(Advanced)'
    if int(rating) == 3:
        return '(Working proficiency)'
    if int(rating) == 2:
        return '(Intermediate)'
    else:
        return '(Elementary)'


@register.filter
def estimate_date(input, value):
    value_list = value.split("-")
    if len(value_list) >= 2:
        return input + relativedelta(months=int(value_list[1]))
    return (input + relativedelta(months=int(12)))


@register.filter
def attachment(input):
    if '.png' in input or '.jpeg' in input or '.jpg' in input or '.gif' in input:
        return "image"
    return 'attachment'
