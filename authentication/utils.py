from django.conf import settings
import random
from django.contrib.auth.models import User
from django_rest_passwordreset.signals import reset_password_token_created
# from django_rest_passwordreset.views import reset_password_request_token
from django.conf import settings
from email.message import EmailMessage
# from django.core.mail import EmailMessage

from smtplib import SMTP_SSL
# from django.dispatch import receiver
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse
from django.conf import settings

def extract_name_components(name):
    components = name.split()  # Split the name into individual words
    # Extract the first name
    first_name = components[0]
    if len(components) == 1:
        # Only first name is available
        return first_name , None ,None
    elif len(components) == 2:
        # First name and last name are available
        last_name = components[1]
        return first_name,None, last_name 
    else:
        # First name, middle name, and last name are available
        middle_name = " ".join(components[1:-1])
        last_name = components[-1]
        return first_name, middle_name, last_name
    


def full_name_components(name):
    components = name.split()  # Split the name into individual words
    
    # Extract the first name
    first_name = components[0]
    
    if len(components) == 1:
        # Only first name is available
        return first_name, None
    else:
        # First name and last name are available
        last_name = ' '.join(components[1:])
        return first_name, last_name
    



# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     # current_site = get_current_site(instance.user)
#     print(instance,"++++")
#     user = reset_password_token.user
#     email_plaintext_message = f"Please click on the following link to reset your password:\n\n" \
#                               f"{reverse('reset-password-confirm', kwargs={'token': reset_password_token.key})}\n\n" \
#                               f"If you didn't request a password reset, please ignore this email.\n\nThank you"

#     email_subject = "Requested For Password Reset"
#     send_email_to_user(user, email_subject, email_plaintext_message)

# def send_email_to_user(user_obj, email_subject, body):
#     user_email = user_obj.email
#     email_sender = settings.DEFAULT_FROM_EMAIL  # Use the default FROM email

#     # Create EmailMessage object
#     email = EmailMessage(
#         subject=email_subject,
#         body=body,
#         from_email=email_sender,
#         to=[user_email],  # List of recipients
#         reply_to=[email_sender]
#     )

#     # Send the email
#     s = email.send(fail_silently=False)
#     print(s,"============")









@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_host = settings.EMAIL_HOST
    if email_host.endswith('/'):
        email_host = email_host[:-1]
    email_plaintext_message = "{}{}?token={}".format(email_host,reverse('reset-password-confirm'), reset_password_token.key)
    email_body = f"Hello {get_full_name(reset_password_token.user)},\n\nPlease click on the following link to reset your password:\n\n{email_plaintext_message}\n\nIf you didn't request a password reset, please ignore this email.\n\nThank you"

    email_subject = "Requested For Paswords Reset"
    send_email_to_user(reset_password_token.user, email_subject, email_body)



def send_email_to_user(user_obj, email_subject, body):
    user_email = user_obj.email
    email_sender = settings.EMAIL_HOST_USER
    email_receiver = user_email
    subject = email_subject
    body = body
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    with SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.sendmail(settings.EMAIL_HOST_USER, user_obj.email, em.as_string())

def generate_username(first_name, last_name = None):
    username = None
    loop_status = True
    i = 100
    fullname = first_name.replace(" ", "").lower()
    if last_name is not None:
        fullname += last_name.replace(" ", "").lower()
    while loop_status:
        username =  fullname + str(random.randint(1, i))
        obj = User.objects.filter(username=username)
        if not obj.exists():
            loop_status = False
        else:
            i += i
    return username


def get_full_name(user_obj):
    fullname = ""
    if user_obj.first_name is not None:
        fullname += user_obj.first_name
    
        if user_obj.last_name is not None or user_obj.last_name != "" or user_obj.last_name != " ":
            fullname += " "+user_obj.last_name
    else:
        fullname += user_obj.email
    
    return fullname








