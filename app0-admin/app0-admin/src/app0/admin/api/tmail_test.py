"""
Platform Tmails: tmail-test
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
from app0.admin.services.tmail_services import get_tmail_by_name
from app0.admin.tmail import TmailSend


SES_CLIENT = "ses"
CHARSET = "UTF-8"
REGION_NAME = "us-east-2"
TEMPLATES_FOLDER: Optional[str] = None
FROM_MAIL: Optional[str] = None
MAILTO_OVERWRITE: Optional[str] = None
BASE_URL: Optional[str] = None
ATTENDANT_URL: Optional[str] = None

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    payload=(TmailSend, "Object Info"),
    responses={
        200: (TmailSend, "Object updated")
    }
)


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER, FROM_MAIL, MAILTO_OVERWRITE, BASE_URL, ATTENDANT_URL
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])
    if FROM_MAIL is None:
        FROM_MAIL = str(context.env["env_config"]["mail_app_from"])
    if MAILTO_OVERWRITE is None:
        MAILTO_OVERWRITE = str(context.env["env_config"]["mailto_overwrite"])
    if BASE_URL is None:
        BASE_URL = str(context.env["env_config"]["app0-admin_url"])
    if ATTENDANT_URL is None:
        ATTENDANT_URL = str(context.env["env_config"]["claimsattendant_url"])


async def run(payload: TmailSend, context: EventContext) -> TmailSend:
    """
    Tmail Run
    """
    es = db(context.env)
    # load mail template
    tmail = await get_tmail_by_name(es, payload.template)
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
    rep[mail.VAR_CLAIMS_APP_URL] = f'{BASE_URL}'
    rep[mail.VAR_PASSWORD_RESET_URL] = f'{BASE_URL}/reset/123456789'
    rep[mail.VAR_EMAIL_CONFIRM_URL] = f'{BASE_URL}/confirm/123456789'

    rep[mail.VAR_COMPANY_LOGO_URL] = 'https://claimsattendant.com/email/images/logo_claims-attendant.png'
    rep[mail.VAR_COMPANY_NAME] = 'SomeCompany'
    rep[mail.VAR_COMPANY_ADDRESS] = '668 NW 5th St, Miami, FL 33128, Estados Unidos'
    rep[mail.VAR_COMPANY_PHONE] = 'Phone: +13053717065'

    rep[mail.VAR_CLAIM_VIEW_URL] = f'{ATTENDANT_URL}/claim/v/123456789'
    rep[mail.VAR_INSPECTION_TYPE] = 'First Inspection'
    rep[mail.VAR_INSPECTION_ADDRESS] = '404 NW 3rd St, Miami, FL 33128, Estados Unidos'
    rep[mail.VAR_INSPECTION_DATE] = 'July 1, 2022, 15:00'
    rep[mail.VAR_CLIENT_NAME] = 'John SomeClient'
    rep[mail.VAR_SPOL_CLIENT_UPLOAD_URL] = f'{ATTENDANT_URL}/claim/u1/123456789'
    rep[mail.VAR_RELEASE_CLIENT_UPLOAD_URL] = f'{ATTENDANT_URL}/claim/u2/123456789'
    rep[mail.VAR_UMPIRE_ACK_CLIENT_UPLOAD_URL] = f'{ATTENDANT_URL}/claim/u3/123456789'
    rep[mail.VAR_RETAINER_CLIENT_UPLOAD_URL] = f'{ATTENDANT_URL}/claim/u4/123456789'

    return rep
