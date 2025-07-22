import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "umairpy1@gmail.com"
EMAIL_PASSWORD = "vdiu wzho hvth bfqo"

def send_otp_email(user):
    subject = "Your Email OTP Verification"
    message = f"Hello {user.name},\n\nYour OTP for verification is: {user.email_otp}\n\nEnter this code to verify your email."

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = user.email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, user.email, msg.as_string())
        server.quit()
        print("✅ OTP sent successfully!")
    except Exception as e:
        print(f"❌ Error sending OTP: {e}")

def send_success_email(email, username):
    subject = "Account Successfully Created - Smart Teacher App"
    message = f"""Dear {username},

Your account has been successfully created and verified on Smart Teacher App.

Welcome aboard!

Regards,
Smart Teacher Team
"""
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        print("✅ Success email sent!")
    except Exception as e:
        print(f"❌ Error sending success email: {e}")
