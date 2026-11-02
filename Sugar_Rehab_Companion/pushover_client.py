"""Pushover delivery without an additional third-party dependency."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def send_push_notification(title: str, message: str) -> str:
    """Submit a plain-text coach alert and report whether Pushover accepted it."""
    token = os.getenv("PUSHOVER_API_TOKEN", "").strip()
    user = os.getenv("PUSHOVER_USER_KEY", "").strip()
    if not token or not user:
        return "Notification not sent: set PUSHOVER_API_TOKEN and PUSHOVER_USER_KEY."
    title, message = title.strip(), message.strip()
    if not title or not message:
        return "Notification not sent: title and message must not be empty."
    if len(title) > 250 or len(message) > 1024:
        return "Notification not sent: title must be at most 250 characters and message at most 1024."

    payload = {"token": token, "user": user, "title": title, "message": message}
    device = os.getenv("PUSHOVER_DEVICE", "").strip()
    if device:
        payload["device"] = device
    request = Request(
        "https://api.pushover.net/1/messages.json",
        data=urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=10) as response:
            result = json.load(response)
            if response.status == 200 and isinstance(result, dict) and result.get("status") == 1:
                return "Coach notification accepted by Pushover."
        return "Notification failed: Pushover did not accept the message."
    except HTTPError as exc:
        return f"Notification failed: Pushover returned HTTP {exc.code}. Check credentials and quota."
    except (URLError, TimeoutError, OSError):
        return "Notification delivery could not be confirmed due to a network error. Do not automatically retry."
    except (ValueError, UnicodeError):
        return "Notification delivery could not be confirmed: invalid Pushover response. Do not automatically retry."
