from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator

class CustomPasswordResetForm(BasePasswordResetForm):
    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html', use_https=False, token_generator=default_token_generator, from_email=None, request=None, html_email_template_name=None, **kwargs):
        # Add expiration time to the context sent to the email template
        expiration_time = timezone.now() + timedelta(minutes=1)  # Set expiration time to 1 day from now
        context = {
            'expiration_time': expiration_time,  # Include expiration time in the context
            # Add other necessary context variables
        }

        # Call the superclass's save method without the 'context' parameter
        super().save(
            domain_override=domain_override,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            **kwargs
        )
