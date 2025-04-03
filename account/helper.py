from django.template.loader import render_to_string
from django.core.mail import send_mail
from premailer import transform

def trigger_email(context, template, subject, recipients, message="Unable to view this, contact admin."):
    try:
        raw_html = render_to_string(template_name=template, context=context)

        html_message = transform(raw_html)

        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            html_message=html_message,
            recipient_list=recipients,
            fail_silently=False
        )
        return None
    except Exception as e:
        return e