"""
Platform TemplateMails: tmail-test
"""
from typing import Optional, Dict
from datetime import datetime, timezone

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3  # type: ignore
import jinja2
from jinja2.loaders import BaseLoader
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

from app0.admin import mail
from app0.admin.db import db
from app0.admin.services.template_mail_services import get_template_mail_by_name
from app0.admin.template_mail import TemplateMailSend


SES_CLIENT = "ses"
CHARSET = "UTF-8"
REGION_NAME = "us-east-2"
TEMPLATES_FOLDER: Optional[str] = None
FROM_MAIL: Optional[str] = None
MAILTO_OVERWRITE: Optional[str] = None
APP0_LOGIN_URL: Optional[str] = None

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    payload=(TemplateMailSend, "Object Info"),
    responses={
        200: (TemplateMailSend, "Object updated")
    }
)


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER, FROM_MAIL, MAILTO_OVERWRITE, APP0_LOGIN_URL
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])
    if FROM_MAIL is None:
        FROM_MAIL = str(context.env["env_config"]["mail_app_from"])
    if MAILTO_OVERWRITE is None:
        MAILTO_OVERWRITE = str(context.env["env_config"]["mailto_overwrite"])
    if APP0_LOGIN_URL is None:
        APP0_LOGIN_URL = str(context.env["env_config"]["app0_admin_url"])


async def run(payload: TemplateMailSend, context: EventContext) -> TemplateMailSend:
    """
    TemplateMail Run
    """
    es = db(context.env)
    # load mail template
    tmail = await get_template_mail_by_name(es, payload.template)
    assert tmail
    # load template
    assert TEMPLATES_FOLDER
    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_FOLDER)
    template_env = jinja2.Environment(loader=template_loader)
    # template for req
    template = template_env.get_template(tmail.template)
    # generate default variables replacements
    payload.replacements = await _set_default_replacements(es, context)
    if tmail.content:
        # replace variables in html content
        body_template = jinja2.Environment(loader=BaseLoader).from_string(tmail.content)  # type: ignore
        body_template_rep = body_template.render(payload.replacements)
        payload.replacements[mail.VAR_CONTENT] = body_template_rep
    # replace variables in template
    content_html = template.render(payload.replacements)
    # send_email
    for destination in payload.destinations:
        msg = MIMEMultipart()
        msg["Subject"] = tmail.subject + f' (Original to {destination})' if MAILTO_OVERWRITE else ''
        msg["From"] = FROM_MAIL
        # only send real name in production
        msg["To"] = MAILTO_OVERWRITE if MAILTO_OVERWRITE else destination

        body = MIMEText(content_html, "html")
        msg.attach(body)

        # Convert message to string and send
        ses_client = boto3.client("ses", region_name=REGION_NAME)
        response = ses_client.send_raw_email(
            Source=FROM_MAIL,
            Destinations=[MAILTO_OVERWRITE if MAILTO_OVERWRITE else destination],
            RawMessage={"Data": msg.as_string()}
        )
        logger.info(context, f"Ses_client: {response}")
        payload.sent_message = str(response)
        payload.sent_date = datetime.now(tz=timezone.utc)
        # TODO save send mail on stream or mongo collection?

    return payload


async def _set_default_replacements(es, context: EventContext) -> Dict[str, str]:
    """default data from test sending"""
    rep: Dict[str, str] = {}

    rep[mail.VAR_USER_NAME] = 'Some User'
    rep[mail.VAR_CLAIMS_APP_URL] = f'{APP0_LOGIN_URL}'
    rep[mail.VAR_PASSWORD_RESET_URL] = f'{APP0_LOGIN_URL}/reset/123456789'
    rep[mail.VAR_EMAIL_CONFIRM_URL] = f'{APP0_LOGIN_URL}/confirm/123456789'

    return rep
