# email_sender.py
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

def send_daily_report(html_path: str, image_path: str):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("ADMIN_EMAIL")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f"Pipeline Report - {datetime.now().strftime('%Y-%m-%d')}"

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    msg.attach(MIMEText(html, 'html'))

    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<chart>')
        msg.attach(img)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()
    print("[Email] Đã gửi báo cáo thành công!")