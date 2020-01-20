from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader

from user.constants import ADMIN
from utils.email import send_email
from employee.models import Employee


@receiver(post_save, sender=Employee)
def create_employee_and_register(sender, instance, **kwargs):
    if kwargs['created']:
        context = {
            'account_type': instance.group,
            'domain': 'http://affarssystem.strativ-support.se'
        }
        email_message = loader.get_template('utils/email_templates/account_invitation.html')
        email_msg = email_message.render(context)
        send_email(subject='invitation', body=email_msg, to=[instance.email])
    else:
        if instance.group.name == ADMIN:
            instance.user.is_staff = True
        else:
            instance.user.is_staff = False
        instance.user.save()
