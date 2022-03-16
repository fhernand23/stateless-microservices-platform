"""
Platform Auth: Validate
"""
from hopeit.app.context import EventContext
from hopeit.app.logger import app_logger

__steps__ = ['validate']

logger = app_logger()
# __api__ = event_api(
#     title="RUBA Auth: Validate",
#     responses={
#         200: (int, "RUBA user_id"),
#     }
# )


async def validate(payload: None, context: EventContext) -> str:
    assert context.auth_info['allowed']
    return context.auth_info['payload']['id_federacion']
