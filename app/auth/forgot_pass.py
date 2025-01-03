import smtplib
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.model import PasswordReset
from app.auth.utils import get_user_by_email, get_password_hash
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
        print(f"Произошла ошибка: {e}")
        raise


async def storage_reset_code(db: AsyncSession, email: str, reset_code: str):
    password_reset = PasswordReset(email=email, reset_code=reset_code)
    db.add(password_reset)
    await db.commit()


async def delete_reset_code(db: AsyncSession, code: str):
    reset_code = await db.execute(select(PasswordReset).filter_by(reset_code=code))
    reset_code = reset_code.scalars().first()
    if not reset_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Код сброса не найден")

    await db.delete(reset_code)

    email = await db.execute(select(PasswordReset).filter_by(email=reset_code.email))
    email = email.scalars().all()
    for e in email:
        await db.delete(e)

    await db.commit()


async def verify_reset_code(db: AsyncSession, code: str):
    res_code = await db.execute(select(PasswordReset).filter_by(reset_code=code))
    reset_code = res_code.scalars().first()

    if not reset_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Код сброса не найден")

    return True if reset_code else False


async def reset_password(db: AsyncSession, email: str, new_password: str):
    user = await get_user_by_email(db, email)
    hashed_pass = get_password_hash(new_password)
    user.hashed_password = hashed_pass
    await db.commit()


async def forgot_password(db: AsyncSession, email: str, code: str = None, new_password: str = None):

    if not code and not new_password and email:
        reset_code = generate_reset_code()
        await send_email(email, "Reset Password", f"Your reset code is: {reset_code}")
        await storage_reset_code(db, email, reset_code)
        return {"detail": "Код сброса отправлен на вашу электронную почту"}
    if code and email and not new_password:
        await verify_reset_code(db, code)
        await delete_reset_code(db, code)
        return {"detail": "Код сброса подтвержден"}
    if new_password and email and not code:
        await reset_password(db, email, new_password)
        return {"detail": "Пароль успешно изменен"}


