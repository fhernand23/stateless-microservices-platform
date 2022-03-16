"""
Platform Registrations: registration-process
"""
import uuid
from dataclasses import dataclass
import traceback
from datetime import datetime, timedelta, timezone
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.fs_storage import FileStorage
from hopeit.dataobjects.payload import Payload
from hopeit.app.client import app_call
from hopeit.dataobjects import dataobject

from app0.admin.common import IdDescription
from app0.admin.company import Company, CompanyConfig
from app0.admin.db import db
from app0.admin.employee import Employee
from app0.admin.registration import Registration
from app0.admin.services import (IDX_COMPANY, IDX_EMPLOYEE, IDX_USER, IDX_COMPANY_CONFIG,
                                 IDX_USER_ROLE, IDX_SUBSCRIPTION, ROLE_COMPANY_ADMIN, ROLE_USER)
from app0.admin.services.registration_services import save_registration
from app0.admin.subscription import BillingInfo, Subscription, PlanInfo
from app0.admin.user import User, UserAppRole
from app0.admin import mail
from app0.admin.tmail import MailTemplate, TmailSend
from app0.platform.auth import AuthReset

logger, extra = app_extra_logger()
DEF_ROLES = [ROLE_COMPANY_ADMIN, ROLE_USER]
DEF_TEAM1 = IdDescription('adjusters', 'Adjusters')
DEF_TEAM2 = IdDescription('managers', 'Managers')
fs_recover: Optional[FileStorage] = None
BASE_URL: Optional[str] = None


@dataobject
@dataclass
class AuthResetData:
    """
    Info for password reset
    """
    user: User
    recovery_token: str


__steps__ = ['run']


class BadRegistration(Exception):
    """Raised when something go wrong"""


async def __init_event__(context: EventContext):
    global fs_recover, BASE_URL
    if fs_recover is None:
        fs_recover = FileStorage(path=str(context.env['fs']['recover_store']))
    if BASE_URL is None:
        BASE_URL = str(context.env["env_config"]["app0-admin_url"])


async def run(payload: Registration, context: EventContext) -> Optional[Subscription]:
    """
    Save
    """
    es = db(context.env)
    subscription = None

    if isinstance(payload, Registration) and payload.status == 'Unprocessed':
        try:
            logger.info(context, f"Processing {payload}")
            # validate registration
            await _validate(es, payload)
            # create company
            company = Company(
                name=payload.company_name, address=payload.company_address, phone_number=payload.company_phone,
                email=payload.company_email, image=payload.company_image)
            await _create_company(es, company)
            # create user & employee
            employee = Employee(
                firstname=payload.firstname, surname=payload.surname, email=payload.email,
                phone_number=payload.phone, position=payload.position,
                teams=[DEF_TEAM1, DEF_TEAM2], address=payload.address,
                owner_id=company.id, owner_name=company.name, company_representative=True)
            user = await _create_employee(es, employee, context)
            # create susbscription
            subscription = await _create_subscription(es, payload, company, user)

        except BadRegistration as ex:
            payload.status = 'Error'
            payload.status_error = str(ex)
        except Exception as ex:  # pylint: disable=W0703
            traceback.print_exc()
            payload.status = 'Error'
            payload.status_error = str(ex)
        else:
            payload.confirm_date = datetime.now().astimezone(timezone.utc)
            payload.company_id = company.id  # type: ignore
            payload.status = 'Confirmed'
        finally:
            await save_registration(es, payload)

    logger.info(context, "Processing complete!")

    return subscription


async def _validate(es, registration: Registration):
    doc = await es[IDX_COMPANY].find_one({'name': {'$eq': registration.company_name}})
    if doc:
        raise BadRegistration('There is already a Company with that name')
    doc = await es[IDX_USER].find_one({'username': {'$eq': registration.email}})
    if doc:
        raise BadRegistration('There is already a User with that email address')


async def _create_company(es, company: Company):
    await es[IDX_COMPANY].replace_one({'_id': ObjectId(company.id)}, Payload.to_obj(company), upsert=True)
    company_config = CompanyConfig(owner_id=company.id, owner_name=company.name)
    await es[IDX_COMPANY_CONFIG].replace_one({'_id': ObjectId(company_config.id)},
                                             Payload.to_obj(company_config),
                                             upsert=True)


async def _create_employee(es, employee: Employee, context: EventContext) -> User:
    """
    Create employee
    """
    await es[IDX_EMPLOYEE].replace_one({'_id': ObjectId(employee.id)}, Payload.to_obj(employee), upsert=True)
    # create user
    user = User(firstname=employee.firstname, surname=employee.surname, username=employee.email,
                email=employee.email, phone_number=employee.phone_number, owner_id=employee.owner_id,
                owner_name=employee.owner_name, employee_id=employee.id, company_representative=True)
    await es[IDX_USER].replace_one({'_id': ObjectId(user.id)}, Payload.to_obj(user), upsert=True)
    # set user roles
    for role in DEF_ROLES:
        user_app_role = UserAppRole(user.username, role)
        await es[IDX_USER_ROLE].replace_one({'_id': ObjectId(user_app_role.id)},
                                            Payload.to_obj(user_app_role), upsert=True)
    # generate token to set password
    await _register(user, context)

    return user


async def _register(user: User, context: EventContext):
    """
    Register user and token with ttl for password setup
    """
    assert fs_recover
    auth_reset = AuthReset(user=user.username, id=user.id,
                           expire=datetime.now(tz=timezone.utc) + timedelta(seconds=3600),
                           first_access=True)
    notify: AuthResetData = AuthResetData(user=user, recovery_token=str(uuid.uuid4()))
    await fs_recover.store(notify.recovery_token, auth_reset)
    logger.info(context, f"User '{notify.user.id}' request password reset")
    # send mail
    tmail_send = TmailSend(
        template=MailTemplate(collection=mail.MAIL_COLLECTION_BASE, name=mail.MAIL_EMAIL_CONFIRMATION),
        destinations=[user.email],
        replacements={
            mail.VAR_USER_NAME: user.firstname + ' ' + user.surname,
            mail.VAR_CLAIMS_APP_URL: f'{BASE_URL}',
            mail.VAR_EMAIL_CONFIRM_URL: f'{BASE_URL}/fset/{notify.recovery_token}',
        },
        files=[])
    logger.info(context, f"Sending Mail {tmail_send}")
    tmail_send_r = await app_call(
        context.event_info.connections[0].app_connection,
        event=context.event_info.connections[0].event,
        datatype=TmailSend, payload=tmail_send, context=context
    )
    logger.info(context, f"Mail queued OK {tmail_send_r}")


async def _create_subscription(es, registration: Registration, company: Company, user: User) -> Subscription:
    """
    Create suscription
    """
    start_date = datetime.now().astimezone(timezone.utc)
    plan = PlanInfo(
        start_date=start_date,
        name=registration.plan_name,  # type: ignore
        description=registration.plan_description,  # type: ignore
        annual_payment=registration.plan_annual_payment,  # type: ignore
        monthly_amount=registration.plan_monthly_amount,  # type: ignore
        annual_amount=registration.plan_annual_amount,  # type: ignore
        max_open_claims=registration.plan_max_open_claims,  # type: ignore
        max_adjusters=registration.plan_max_adjusters,  # type: ignore
        max_storage=registration.plan_max_storage  # type: ignore
    )
    billing = BillingInfo(
        card_holder='NO INFORMATION',
        card_id='0000000000'
    )
    subscription = Subscription(start_date=start_date, registration=registration, plan=plan,
                                billing=billing, user_id=user.id,  # type: ignore
                                user_name=user.firstname + ' ' + user.surname,
                                company_id=company.id, company_name=company.name)  # type: ignore
    await es[IDX_SUBSCRIPTION].replace_one({'_id': ObjectId(subscription.id)},
                                           Payload.to_obj(subscription), upsert=True)
    return subscription
