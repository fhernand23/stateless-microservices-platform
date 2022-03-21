"""
Platform Services: mail-processor
"""
import os
from io import BytesIO
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional, Union

import boto3  # type: ignore
import jinja2
from jinja2.loaders import BaseLoader
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

from app0.admin.db import db
from app0.admin.services.template_mail_services import get_template_mail_by_name
from app0.admin.template_mail import MailAttachment, TemplateMailSend
from app0.admin import mail
from app0.admin.util.object_storage import ObjectStorage, ObjectStorageConf, ObjectStorageConnConfig

SES_CLIENT = "ses"
CHARSET = "UTF-8"
REGION_NAME = "us-east-2"
TEMPLATES_FOLDER: Optional[str] = None
FROM_MAIL: Optional[str] = None
MAILTO_OVERWRITE: Optional[str] = None
MAIL_ATTACH_OVERWRITE: Optional[str] = None
company_object_store: Optional[ObjectStorage] = None
claims_object_store: Optional[ObjectStorage] = None

logger, extra = app_extra_logger()
__steps__ = ['process']


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER, FROM_MAIL, MAILTO_OVERWRITE, MAIL_ATTACH_OVERWRITE
    global company_object_store, claims_object_store
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])
    if FROM_MAIL is None:
        FROM_MAIL = str(context.env["env_config"]["mail_app_from"])
    if MAILTO_OVERWRITE is None:
        MAILTO_OVERWRITE = str(context.env["env_config"]["mailto_overwrite"])
    if MAIL_ATTACH_OVERWRITE is None:
        MAIL_ATTACH_OVERWRITE = str(context.env["env_config"]["mail_attach_overwrite"])
    # due to some bug on hopeit.engine, context.settings don't load 'settings' in Streams
    # changed to 'env'
    # conn_config: ObjectStorageConnConfig = context.settings(key='data_store', datatype=ObjectStorageConnConfig)
    conn_config: ObjectStorageConnConfig = ObjectStorageConnConfig(  # type: ignore
        aws_access_key_id=context.env["data_store"]["aws_access_key_id"],  # type: ignore
        aws_secret_access_key=context.env["data_store"]["aws_secret_access_key"],  # type: ignore
        endpoint_url=context.env["data_store"]["endpoint_url"])  # type: ignore
    if company_object_store is None:
        # company_bucket: ObjectStorageConf = context.settings(key='company_docs', datatype=ObjectStorageConf)
        company_bucket: ObjectStorageConf = ObjectStorageConf(
            bucket=context.env["company_docs"]["bucket"],  # type: ignore
            chunk_size=context.env["company_docs"]["chunk_size"])  # type: ignore
        company_object_store = await ObjectStorage().connect(conn_config=conn_config, bucket=company_bucket.bucket)
    if claims_object_store is None:
        # claims_bucket: ObjectStorageConf = context.settings(key='claims_docs', datatype=ObjectStorageConf)
        claims_bucket: ObjectStorageConf = ObjectStorageConf(
            bucket=context.env["claims_docs"]["bucket"],  # type: ignore
            chunk_size=context.env["claims_docs"]["chunk_size"])  # type: ignore
        claims_object_store = await ObjectStorage().connect(conn_config=conn_config, bucket=claims_bucket.bucket)


async def process(payload: TemplateMailSend, context: EventContext):
    """
    Save
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
            msg["Subject"] = tmail.subject + f' (Original to {destination})' if MAILTO_OVERWRITE else ''
            msg["From"] = FROM_MAIL
            # only send real name in production
            msg["To"] = MAILTO_OVERWRITE if MAILTO_OVERWRITE else destination

            body = MIMEText(content_html, "html")
            msg.attach(body)

            # get file attachments from buckets
            attachments: dict[str, Union[BytesIO, bytes]] = await _get_attachments(payload.files, context)
            for filenamename, attach in attachments.items():
                part = MIMEApplication(attach.getvalue() if isinstance(attach, BytesIO) else attach)
                part.add_header("Content-Disposition", "attachment", filename=filenamename)
                msg.attach(part)

            # Convert message to string and send
            ses_client = boto3.client(SES_CLIENT, region_name=REGION_NAME)
            response = ses_client.send_raw_email(
                Source=FROM_MAIL,
                Destinations=[MAILTO_OVERWRITE if MAILTO_OVERWRITE else destination],
                RawMessage={"Data": msg.as_string()}
            )
            # TODO save sended mail on stream or mongo collection for audit?
            # TODO write to disc
            logger.info(context, f"Ses_client OK: {response}")
        except (Exception, IOError) as e:  # pylint: disable=broad-except
            # TODO save error log if not sended
            # TODO write to disc
            logger.warning(context, f"Ses_client ERROR {e}")


async def _get_attachments(files: List[MailAttachment], context: EventContext) -> dict[str, Union[BytesIO, bytes]]:
    """
    Load attachments from object store
    """
    attachments: dict[str, Union[BytesIO, bytes]] = {}
    assert claims_object_store
    assert company_object_store
    if files:
        for file in files:
            attachfilename = file.doc_name
            _, fextension = os.path.splitext(file.doc_id)
            if not attachfilename.endswith(fextension):
                attachfilename += fextension

            if MAIL_ATTACH_OVERWRITE and MAIL_ATTACH_OVERWRITE != 'None':
                # attach dummy file
                with open(MAIL_ATTACH_OVERWRITE, "rb") as file_obj:
                    attachments[attachfilename] = file_obj.read()
            else:
                # get real file from S3
                try:
                    file_obj = BytesIO()
                    if file.claim_id:
                        s3_obj_id = f"{file.owner_id}/{file.claim_id}/{file.doc_id}"
                        logger.info(context, f"Getting s3 resource: {s3_obj_id}")
                        await claims_object_store.get(s3_obj_id, file_obj)
                        logger.info(context, "S3 resource getted OK")
                        attachments[attachfilename] = file_obj
                    else:
                        s3_obj_id = f"{file.doc_id}"
                        logger.info(context, f"Getting s3 resource: {s3_obj_id}")
                        await company_object_store.get(s3_obj_id, file_obj)
                        logger.info(context, "S3 resource getted OK")
                        attachments[attachfilename] = file_obj
                except Exception as e:  # pylint: disable=broad-except
                    logger.warning(context, f"S3 get ERROR {e}")

    return attachments
