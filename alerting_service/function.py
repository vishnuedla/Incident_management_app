import smtplib
from email.message import EmailMessage

class Email:
    SMTP_HOST = "smtp.aol.com"
    SMTP_PORT = 587
    USERNAME = "edlavishnu@aol.com"
    PASSWORD = "xotp pyqk cgwg ayga"  # App password

    def __init__(self, INCIDENT,DEPARTMENT, ISSUE, ENVIRONMENT , DESCRIPTION , PRIORITY):
        self.INCIDENT= INCIDENT
        self.DEPARTMENT = DEPARTMENT
        self.ISSUE = ISSUE
        self.ENVIRONMENT = ENVIRONMENT
        self.DESCRIPTION = DESCRIPTION
        self.PRIORITY = PRIORITY    

    def build_message(self):
        msg = EmailMessage()
        msg['Subject'] = f'Incident Alert: {self.INCIDENT}'
        msg['From'] = self.USERNAME
        msg['To'] = "edlavishnu2000@gmail.com"
        msg.set_content(
            f"Hello Team,\n\n"
            f"Incident ID : {self.INCIDENT}\n"
            f"Department: {self.DEPARTMENT}\n"
            f"PRIORITY: {self.PRIORITY}\n"
             f"ISSUE: {self.ISSUE}\n\n"
            F"ENVIRONMENT : {self.ENVIRONMENT}\n"
            f"DESCRIPTION: {self.DESCRIPTION}\n"

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