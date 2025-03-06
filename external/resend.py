import os

import resend
import dotenv
from inngest import NonRetriableError

dotenv.load_dotenv()
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
resend.api_key = RESEND_API_KEY


async def send_email(to: str, subject: str, html: str) -> None:
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to,
            "subject": subject,
            "html": html
        })
    except Exception as e:
        raise NonRetriableError(f"Resend API request failed: {e}")
