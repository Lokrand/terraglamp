from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template

import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr

load_dotenv()

smtp_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM", "terraglamp"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class UserEmail(BaseModel):
    email: EmailStr
    subject: str
    text: str


def render_template(template_filename, context):
    with open(template_filename, encoding="utf-8") as file_:
        template = Template(file_.read())
    return template.render(context)


async def send_email(email: str, subject: str, mail_text: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        html=mail_text,
        subtype="html",
    )
    fm = FastMail(smtp_conf)
    await fm.send_message(message)


def render_notification_text(dw_link, user_id):
    return render_template(
        "src/frontend/templates/mail_notify.html",
        {
            "dw_link": dw_link,
            "host": "https://savespotifydw.duckdns.org/",
            "unsubscribe": f"https://savespotifydw.duckdns.org/#/user/{user_id}",
        },
    )


def render_save_pl_text(dw_link, user_id):
    return render_template(
        "src/frontend/templates/mail_save_pl.html",
        {
            "dw_link": dw_link,
            "host": "https://savespotifydw.duckdns.org/",
            "unsubscribe": f"https://savespotifydw.duckdns.org/#/user/{user_id}",
        },
    )
