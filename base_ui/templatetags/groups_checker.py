from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """ Template tag to check if user have a given group """
    return user.groups.filter(name=group_name).exists()
