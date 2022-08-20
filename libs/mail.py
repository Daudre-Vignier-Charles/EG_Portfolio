import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class Message:
    def __init__(self, from_addr, to_addr, subject, message):
        self.msg = MIMEMultipart()
        self.msg['From'] = from_addr
        self.msg['To'] = to_addr
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(message))

    def attach_file(self, file, filename):
        attachment = MIMEApplication(file.read(), Name=filename)
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        self.msg.attach(attachment)

    def from_msg(self):
        return self.msg["From"]

    def to_msg(self):
        return self.msg["To"]

    def message(self):
        return self.msg


class MailSenderConfig:
    def __init__(self, server, login, password, port=0, starttls=False, ssl=True):
        self.server = server
        self.login = login
        self.password = password
        self.port = port
        self.starttls = starttls
        self.ssl = ssl


class MailSender:
    def __init__(self, mail_server_config: MailSenderConfig):
        if mail_server_config.ssl:
            self.mailserver = smtplib.SMTP_SSL(host=mail_server_config.server, port=mail_server_config.port)
        else:
            self.mailserver = smtplib.SMTP(host=mail_server_config.server, port=mail_server_config.port)
        if mail_server_config.starttls:
            self.mailserver.starttls()
        self.mailserver.login(mail_server_config.login, mail_server_config.password)

    def send_mail(self, msg: Message):
        self.mailserver.sendmail(msg.from_msg(), msg.to_msg(), msg.message().as_string())
