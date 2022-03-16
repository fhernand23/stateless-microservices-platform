"""
Platform Tmails: tmail-send
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

from app0.admin.tmail import TmailSend

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
    return payload
