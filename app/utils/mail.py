from flask import current_app, render_template
import resend


from app.config import Config


def send_email(to, subject, template, **kwargs):
    resend.api_key = Config.RESEND_API_KEY

    params: resend. Emails. SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": to,
        "subject": subject,
        "html": template
    }

    email = resend.Emails.send(params)
    print(email)

def send_welcome_email(user):
    """Sends a welcome email to the new user."""
    try:
        return send_email(
            to=user.email,
            subject="Welcome to Our Service!",
            template="Welcome",
            username=user.username,
        )
    except Exception as e:
        return False