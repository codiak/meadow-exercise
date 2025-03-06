import os

import resend
from inngest import NonRetriableError

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
resend.api_key = RESEND_API_KEY


async def send_email(to: str, subject: str, html: str) -> str:
    try:
        email = resend.Emails.send({
            "from": "onboarding@resend.dev",  # TODO: Use an address on the correct domain
            "to": to,
            "subject": subject,
            "html": html
        })
        return email['id']
    except Exception as e:
        raise NonRetriableError(f"Resend API request failed: {e}")
