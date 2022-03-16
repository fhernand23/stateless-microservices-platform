"""
Platform Registrations: registration-pub-save
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

from app0.admin.db import db
from app0.admin.registration import Registration
from app0.admin.services.registration_services import save_registration

logger, extra = app_extra_logger()

__steps__ = ['run']

__api__ = event_api(
    payload=(Registration, "Object Info"),
    responses={
        200: (Registration, "Object updated"),
        400: (str, "Request error"),
    }
)


async def run(payload: Registration, context: EventContext) -> Registration:
    """
    Save Registration
    """
    es = db(context.env)
    logger.info(context, f"Public registration {payload}")
    await save_registration(es, payload)

    return payload
