# email_sender.py
import smtplib
from email.mime.text import MIMEText

def send_email(to_address, subject, body, host, port, username, password):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = username
        msg['To'] = to_address

        server = smtplib.SMTP(host, port, timeout=10)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, [to_address], msg.as_string())
        server.quit()
        return True, None
    except Exception as e:
        return False, str(e)
