"""

E-mail notifications sender

"""
import smtplib

import settings


def sent_notification(path_to_file: str) -> None:
    """
    Send e-mail notifications
    """
    message = f"""
    From: Text parser
    Subject: Parsing error

    Wrong file format: {path_to_file}
    """

    smtp = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    smtp.sendmail(settings.MAIL_SENDER, settings.MAIL_RECEIVERS, message)
    smtp.quit()
