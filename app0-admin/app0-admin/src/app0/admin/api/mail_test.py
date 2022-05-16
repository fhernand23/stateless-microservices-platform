"""
Platform Tmails: tmail-test
"""
from typing import Optional, Dict
from datetime import datetime, timezone

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
from jinja2.loaders import BaseLoader

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.fs_storage import FileStorage

from app0.admin import mail
from app0.admin.db import db
from app0.admin.services.tmail_services import get_tmail_by_name
from app0.admin.tmail import TmailSend


CHARSET = "UTF-8"
TEMPLATES_FOLDER: Optional[str] = None
FROM_MAIL: Optional[str] = None
APP0_ADMIN_URL: Optional[str] = None

logger, extra = app_extra_logger()
fs_mail: Optional[FileStorage] = None

__steps__ = ['run']
__api__ = event_api(
    payload=(TmailSend, "Object Info"),
    responses={
        200: (TmailSend, "Object updated")
    }
)


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER, FROM_MAIL, APP0_ADMIN_URL, fs_mail
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])
    if FROM_MAIL is None:
        FROM_MAIL = str(context.env["env_config"]["mail_app_from"])
    if APP0_ADMIN_URL is None:
        APP0_ADMIN_URL = str(context.env["env_config"]["app0_admin_url"])
    if fs_mail is None:
        fs_mail = FileStorage(path=str(context.env['fs']['mail_store']))


async def run(payload: TmailSend, context: EventContext) -> TmailSend:
    """
    Tmail Run
    """
    es = db(context.env)
    # load mail template
    tmail = await get_tmail_by_name(es, payload.template)
    assert tmail and fs_mail
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
        msg["Subject"] = tmail.subject
        msg["From"] = FROM_MAIL
        # only send real name in production
        msg["To"] = destination

        body = MIMEText(content_html, "html")
        msg.attach(body)

        # write to disc for now, you can send the mail by an api
        mailkey = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{destination}"
        await fs_mail.store(key=f"{mailkey}_{destination}", value=msg.as_string())
        logger.info(context, f"Mail send OK: {mailkey}")
        payload.sent_message = 'OK'
        payload.sent_date = datetime.now(tz=timezone.utc)

    return payload


async def _set_default_replacements(es, context: EventContext) -> Dict[str, str]:
    """default data from test sending"""
    rep: Dict[str, str] = {}

    rep[mail.VAR_USER_NAME] = 'Some User'
    rep[mail.VAR_ADMIN_APP_URL] = f'{APP0_ADMIN_URL}'
    rep[mail.VAR_PASSWORD_RESET_URL] = f'{APP0_ADMIN_URL}/reset/123456789'
    rep[mail.VAR_EMAIL_CONFIRM_URL] = f'{APP0_ADMIN_URL}/confirm/123456789'

    return rep
