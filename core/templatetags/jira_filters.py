from django import template

register = template.Library()


@register.filter(name='second_to_hour')
def second_to_hour(seconds):
    """Receives seconds and convert it into hour"""
    hour = int(seconds / 3600)
    minute = int(int(seconds % 3600) / 60)
    human_time = ''
    if hour:
        human_time = str(hour) + ' hour'
        if hour > 1:
            human_time += 's'
        human_time += ' '

    if minute:
        human_time += str(minute) + ' minute'
        if minute > 1:
            human_time += 's'
    if human_time != '':
        return human_time

    return '--'
