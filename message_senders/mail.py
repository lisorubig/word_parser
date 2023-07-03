import smtplib
import settings


def sent_notification(data: bytes) -> None:
    message = f"""
    From: Text parser
    Subject: Parsing error

    Wrong file format: {data}
    """

    smtp = smtplib.SMTP(settings.SMTP_SERVER)
    smtp.sendmail(settings.MAIL_SENDER, settings.MAIL_RECEIVERS, message)
    print("Successfully sent email")
