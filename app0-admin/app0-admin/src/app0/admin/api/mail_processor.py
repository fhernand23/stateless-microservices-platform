"""
Platform Services: mail-processor
"""
from datetime import datetime
from typing import Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jinja2
from jinja2.loaders import BaseLoader
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.fs_storage import FileStorage

from app0.admin.db import db
from app0.admin.services.tmail_services import get_tmail_by_name
from app0.admin.tmail import TmailSend
from app0.admin import mail

SES_CLIENT = "ses"
CHARSET = "UTF-8"
REGION_NAME = "us-east-2"
TEMPLATES_FOLDER: Optional[str] = None
FROM_MAIL: Optional[str] = None

logger, extra = app_extra_logger()
fs_mail: Optional[FileStorage] = None

__steps__ = ['process']


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER, FROM_MAIL, fs_mail
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])
    if FROM_MAIL is None:
        FROM_MAIL = str(context.env["env_config"]["mail_app_from"])
    if fs_mail is None:
        fs_mail = FileStorage(path=str(context.env['fs']['mail_store']))


async def process(payload: TmailSend, context: EventContext):
    """
    Save
    """
    es = db(context.env)
    # load mail template
    tmail = await get_tmail_by_name(es, payload.template)
    assert tmail and TEMPLATES_FOLDER and fs_mail
    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_FOLDER)
    template_env = jinja2.Environment(loader=template_loader)
    # template for req
    template = template_env.get_template(tmail.template)
    if tmail.content:
        # replace variables in html content
        body_template = jinja2.Environment(loader=BaseLoader).from_string(tmail.content)  # type: ignore
        body_template_rep = body_template.render(payload.replacements)
        payload.replacements[mail.VAR_CONTENT] = body_template_rep  # type: ignore
    # replace variables in template
    content_html = template.render(payload.replacements)
    # send_email
    for destination in payload.destinations:
        try:
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
        except (Exception, IOError) as e:  # pylint: disable=broad-except
            # TODO save error log if not sended
            # TODO write to disc
            logger.warning(context, f"Mail send ERROR {e}")
