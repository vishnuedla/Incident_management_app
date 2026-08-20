import smtplib
from email.message import EmailMessage


def email_alert(INCIDENT_ID, DESCRIPTION, DEPARTMENT, STATUS):
    msg = EmailMessage()
    msg['Subject'] = f'Incident Alert: {INCIDENT_ID}'
    msg['From'] = 'edlavishnu@aol.com'
    msg.set_content(
        "Hello Team,\n\n"
        f"DESCRIPTION: {DESCRIPTION}\n"
        f"Department: {DEPARTMENT}\n"
        f"STATUS: {STATUS}\n\n"
        "Regards,\nIncident Management alerting Team"
    )
    msg['To'] = 'edlavishnu2000@gmail.com'
    server = smtplib.SMTP('smtp.aol.com', 587)
    server.starttls()
    server.login(
        'edlavishnu@aol.com',
        'xotp pyqk cgwg ayga'
    )
    server.send_message(msg)
    server.quit()