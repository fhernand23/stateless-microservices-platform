"""
Platform Tmails: tmail-send
"""
from bson.objectid import ObjectId  # type: ignore

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.dataobjects.payload import Payload

from app0.admin.db import db
from app0.admin.tmail import TmailSend, MailLog
from app0.admin.util import app_util
from app0.admin.notification import Notification
from app0.admin.services import IDX_NOTIFICATION

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    payload=(TmailSend, "Object Info"),
    responses={
        200: (TmailSend, "Object updated")
    }
)


async def run(payload: TmailSend, context: EventContext) -> TmailSend:
    """
    Only return TmailSend to write in stream
    """
    es = db(context.env)
    for destination in payload.destinations:
        await _save_notification(es, MailLog(subject=payload.template.name, destination=destination))
    return payload


async def _save_notification(es, mail_log: MailLog):
    """Save notification of queue mail log"""
    notification = Notification(
        creation_date=mail_log.log_date,
        user_id=app_util.SYSTEM_USER,
        user_name=app_util.SYSTEM_USER_DESC,
        app_name=app_util.APP_ADMIN,
        type=app_util.TYPE_MAIL,
        content=f"Mail {mail_log.subject} to {mail_log.destination} has been queued")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification.id)},
                                           Payload.to_obj(notification),
                                           upsert=True)
