import os
import smtplib
import logging
from email.message import EmailMessage
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


EMAIL_ENABLED: bool = os.getenv("EMAIL_ENABLED", "false").lower() == "true"

SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
try:
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 465))
except ValueError:
    logging.exception("Invalid SMTP_PORT value")
    raise
SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
EMAIL_TO: Optional[str] = os.getenv("EMAIL_TO")


def is_email_config_valid():
    """Check if all required email configuration values are set."""
    return all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAIL_TO])


def send_email_alert(subject: str, body: str) -> None:
    global EMAIL_ENABLED
    if not is_email_config_valid():
        logging.warning("Email settings are incomplete. Skipping email.")
        return

    if not EMAIL_ENABLED:
        return

    try:

        msg = EmailMessage()
        msg["From"] = SMTP_USER
        msg["To"] = EMAIL_TO
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:

            # For encrypted email:
            # - SMTP_SSL: implicit TLS, usually port 465
            # - SMTP + STARTTLS: explicit TLS upgrade, usually port 587

            server.login(SMTP_USER, SMTP_PASSWORD)

            server.send_message(msg)

    except smtplib.SMTPAuthenticationError:
        EMAIL_ENABLED = False
        logging.exception("SMTP authentication failed. Disabling email alerts.")
        raise

    except smtplib.SMTPException:
        logging.exception("Temporary SMTP error")
