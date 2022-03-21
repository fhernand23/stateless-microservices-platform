"""
Platform TemplateMails: tmail-send
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

from app0.admin.template_mail import TemplateMailSend

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    payload=(TemplateMailSend, "Object Info"),
    responses={
        200: (TemplateMailSend, "Object updated")
    }
)


async def run(payload: TemplateMailSend, context: EventContext) -> TemplateMailSend:
    """
    Only return TemplateMailSend to write in stream
    """
    return payload
