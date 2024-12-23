import smtplib
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.model import PasswordReset
from app.config import SENDER_MAIL, SENDER_PASS
import random


def generate_reset_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


async def send_email(to_email: str, subject: str, body: str):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = SENDER_MAIL
    sender_name = "Admin"
    sender_password = SENDER_PASS

    try:
        message = MIMEMultipart()
        message["From"] = formataddr((sender_name, sender_email))
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise


async def storage_reset_code(db: AsyncSession, email: str, reset_code: str):
    password_reset = PasswordReset(email=email, reset_code=reset_code)
    db.add(password_reset)
    await db.commit()


async def delete_reset_code(db: AsyncSession, email: str):
    email_code = await db.execute(select(PasswordReset).filter_by(email=email))
    email_code = email_code.scalars().first()
    if not email_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reset code not found")

    await db.delete(email_code)
    await db.commit()


async def verify_reset_code(db: AsyncSession, code: str):
    res_code = await db.execute(select(PasswordReset).filter_by(reset_code=code))
    reset_code = res_code.scalars().first()

    if not reset_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid reset code")

    return True if reset_code else False


async def forgot_password(db: AsyncSession, email: str, code: str = None):
    print('I am in forgot pass')

    if not code:
        reset_code = generate_reset_code()
        await send_email(email, "Reset Password", f"Your reset code is: {reset_code}")
        await storage_reset_code(db, email, reset_code)
        return {"detail": "Reset code sent to your email"}
    else:
        await verify_reset_code(db, code)
        await delete_reset_code(db, email)
        return {"detail": "Password reset successfully"}


