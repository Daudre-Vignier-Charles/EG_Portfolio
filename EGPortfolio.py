import io
import datetime
from os.path import basename

from config import cfg_estateguru, cfg_mailserver, cfg_message
from libs.EGPortfolioScraper import Scraper
from libs.mail import Message, MailSenderConfig, MailSender

print("Getting date and time")
today = datetime.datetime.today()
print("Initializing scraper")
scraper = Scraper(cfg_estateguru["login"], cfg_estateguru["password"])
print("Scrapping portfolio")
portfolio = scraper.get_portfolio()
print("Creating mail sender config")
mail_sender_config = MailSenderConfig(
    cfg_mailserver["server"],
    cfg_mailserver["login"],
    cfg_mailserver["password"],
    ssl = cfg_mailserver["ssl"],
    starttls = cfg_mailserver["starttls"],
    port = cfg_mailserver["port"]
    )
print("Initializing mail sender")
mail_sender = MailSender(mail_sender_config)
print("Building message")
message = Message(
    cfg_message["from"],
    cfg_message["to"],
    "EstateGuru Portfolio {}".format(today.strftime("%d-%m-%Y")),
    "Portefeuille EstateGuru - scrapé le {} à {}".format(today.strftime("%d-%m-%Y"), today.strftime("%H:%M:%S")),
    )
print("Converting bytes to virtual file")
pfile = io.BytesIO(portfolio)
print("Attaching virtual file")
message.attach_file(pfile, "EGPortfolio_{}.xls".format(today.strftime("%d-%m-%Y")))
print("Sending message")
mail_sender.send_mail(message)
