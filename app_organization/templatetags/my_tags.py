from django import templatefrom django.contrib.auth.models import User, AnonymousUserfrom app_organization.models import OrgMembersregister = template.Library()@register.filterdef cap_please(value: str):    return value.capitalize()@register.filterdef replace(value: str, arg):    if not isinstance(value, str):        raise Exception("Type doesn't match")    return value.replace(arg, ' ozgartirib qoydik brat ')def check_for_groups(user: User, arg: str):    groups = arg.split(',')    for group in groups:        if OrgMembers.objects.filter(user=user.id, role=group).exists():            # if user.groups.filter(name=group).exists():            return True    return False@register.filterdef has_group(user, arg: str):    if not isinstance(user, User) and not isinstance(user, AnonymousUser):        raise Exception("Type doesn't match")    if user.is_anonymous:        return False    return check_for_groups(user, arg)