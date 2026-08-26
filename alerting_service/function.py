import smtplib
from email.message import EmailMessage

class Email:
    SMTP_HOST = "smtp.aol.com"
    SMTP_PORT = 587
    USERNAME = "edlavishnu@aol.com"
    PASSWORD = "xotp pyqk cgwg ayga"  # App password

    def __init__(self, incident_id, description, department, status):
        self.incident_id = incident_id
        self.description = description
        self.department = department
        self.status = status

    def build_message(self):
        msg = EmailMessage()
        msg['Subject'] = f'Incident Alert: {self.incident_id}'
        msg['From'] = self.USERNAME
        msg['To'] = "edlavishnu2000@gmail.com"
        msg.set_content(
            f"Hello Team,\n\n"
            f"DESCRIPTION: {self.description}\n"
            f"Department: {self.department}\n"
            f"STATUS: {self.status}\n\n"
            "Regards,\nIncident Management alerting Team"
        )
        return msg

    @classmethod
    def email_connection(cls):
        server = smtplib.SMTP(cls.SMTP_HOST, cls.SMTP_PORT)
        server.starttls()
        server.login(cls.USERNAME, cls.PASSWORD)
        return server

    def send_email(self):
        conn = self.email_connection()
        msg = self.build_message()
        conn.send_message(msg)
        conn.quit()
        print("✅ Email sent successfully")