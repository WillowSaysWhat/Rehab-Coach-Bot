import os
import logging
from pathlib import Path

import resend
from dotenv import load_dotenv
from resend.exceptions import ResendError

logger = logging.getLogger(__name__)

def send_email(subject: str, html: str) -> str:
    """Send an email to the coach with an agent-written subject and HTML content."""
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    api_key = os.getenv("RESEND_API_KEY", "").strip()
    if not api_key:
        return "Email not sent: set RESEND_API_KEY in .env."
    if not subject.strip() or not html.strip():
        return "Email not sent: subject and html must not be empty."
    resend.api_key = api_key
    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "willowsayswhat@gmail.com",
            "subject": subject,
            "html": html,
        })
    except ResendError as exc:
        # Keep credentials out of diagnostics, even if a provider echoes them.
        detail = str(exc).replace(api_key, "[redacted]")
        result = f"Resend rejected the email (HTTP {exc.code}): {detail}"
        logger.error("%s", result)
        return result
    except Exception as exc:
        logger.error("Resend delivery could not be confirmed (%s).", type(exc).__name__)
        return "Email delivery could not be confirmed by Resend. Do not automatically retry."
    if not isinstance(response, dict) or not response.get("id"):
        return "Email delivery could not be confirmed: Resend returned no email ID."
    logger.warning("Resend accepted coach email; email ID: %s", response["id"])
    return f"Email accepted by Resend for willowsayswhat@gmail.com. Email ID: {response['id']}"
