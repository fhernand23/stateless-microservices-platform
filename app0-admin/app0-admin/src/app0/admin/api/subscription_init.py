"""
Platform Subscription: subscription-init
"""
from datetime import datetime, timezone
import os
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.dataobjects.payload import Payload

from app0.admin.company import Company
from app0.admin.damage import Damage
from app0.admin.db import db
from app0.admin.enums import Enum, config_path
from app0.admin.http import HttpRespInfo
from app0.admin.insurance import InsuranceCompany
from app0.admin.notification import Notification
from app0.admin.services import (IDX_COMPANY, IDX_COMPANY_MAIL, IDX_DAMAGE,
                                  IDX_INSURANCE_COMPANY, IDX_NOTIFICATION,
                                  IDX_USER)
from app0.admin.subscription import Subscription
from app0.admin.tmail import Tmail
from app0.admin.user import User
from app0.admin.util import company_util

BaseDamages = Enum.load_csv(config_path, "BaseDamages", '*')
BaseInsuranceCompanies = Enum.load_csv(config_path, "BaseInsuranceCompanies", '*')
BaseMails = Enum.load_csv(config_path, "BaseMails", '*')
TEMPLATES_FOLDER: Optional[str] = None

logger, extra = app_extra_logger()
__steps__ = ['run']


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])


async def run(payload: Subscription, context: EventContext) -> HttpRespInfo:
    """Save"""
    logger.info(context, "Subscription init START!")
    if payload:
        es = db(context.env)

        logger.info(context, f"Init {payload}")
        # get company
        colc = es[IDX_COMPANY]
        docc = await colc.find_one(ObjectId(payload.company_id))
        company = Payload.from_obj(docc, Company)
        # get user
        colu = es[IDX_USER]
        docu = await colu.find_one(ObjectId(payload.user_id))
        user = Payload.from_obj(docu, User)
        # create notifications
        await _create_notification_company(es, company)
        await _create_notification_user(es, user)
        # create base data
        await _create_tmails(es, company)
        await _create_damages(es, company)
        await _create_ins_companies(es, company)

        logger.info(context, "Processing complete!")

    return HttpRespInfo(200, 'OK')


async def _create_notification_company(es, company: Company):
    """
    Create Notification for Company
    """
    assert company.id
    notification = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=company_util.SYSTEM_USER,
        user_name=company_util.SYSTEM_USER_DESC,
        owner_id=company.id,
        owner_name=company.name,
        app_name=company_util.APP_BASE,
        content=f"Company {company.name} has been added to Claims Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification.id)},
                                           Payload.to_obj(notification),
                                           upsert=True)


async def _create_notification_user(es, user: User):
    """
    Create Notification for User
    """
    notification = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=company_util.SYSTEM_USER,
        user_name=company_util.SYSTEM_USER_DESC,
        owner_id=user.owner_id if user.owner_id else "",
        owner_name=user.owner_name if user.owner_name else "",
        app_name=company_util.APP_BASE,
        content=f"User {user.email} has been added to Claims Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification.id)},
                                           Payload.to_obj(notification),
                                           upsert=True)

    notification2 = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=company_util.SYSTEM_USER,
        user_name=company_util.SYSTEM_USER_DESC,
        owner_id=user.owner_id if user.owner_id else "",
        owner_name=user.owner_name if user.owner_name else "",
        type=company_util.TYPE_DIRECT,
        app_name=company_util.APP_BASE,
        dest_user_id=user.id,  # type: ignore
        content=f"Welcome {user.email} to the Claims Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification2.id)},
                                           Payload.to_obj(notification2),
                                           upsert=True)


async def _create_company(es, company: Company):
    """Create Company"""
    await es[IDX_COMPANY].replace_one({'_id': ObjectId(company.id)}, Payload.to_obj(company), upsert=True)
    return company


async def _create_tmails(es, company: Company):
    """Create mail templates for company"""
    assert company.id
    for d in BaseMails:
        did = d['id']
        email = Tmail(
            name=d['name'],
            subject=d['subject'],
            template=d['template'],
            description=d['description'],
            tags=[d['tag']])
        email.content = await _load_mail_base_content(did)
        email.owner_id = company.id
        email.owner_name = company.name
        await es[IDX_COMPANY_MAIL].replace_one({'_id': ObjectId(email.id)}, Payload.to_obj(email), upsert=True)


async def _load_mail_base_content(did):
    assert TEMPLATES_FOLDER
    file_path = os.path.join(TEMPLATES_FOLDER, did + '_base_content.txt')
    if os.path.isfile(file_path):
        file = open(file_path, "r", encoding="utf-8")
        cont = file.read()
        file.close()
        return cont
    return ''


async def _create_damages(es, company: Company):
    damages = [Damage(name=d['name'], category=d['category']) for d in BaseDamages]
    assert company.id
    for d in damages:
        d.owner_id = company.id
        d.owner_name = company.name
        await es[IDX_DAMAGE].replace_one({'_id': ObjectId(d.id)}, Payload.to_obj(d), upsert=True)


async def _create_ins_companies(es, company: Company):
    """
    Create Insurrance Company
    """
    for bic in BaseInsuranceCompanies:
        ic = InsuranceCompany(name=bic['name'])
        ic.address = bic['address']
        ic.aptsuiteunit = bic['aptsuiteunit']
        ic.city = bic['city']
        ic.state = bic['state']
        ic.zipcode = bic['zipcode']
        ic.phone_number = bic['phone1']
        ic.email = bic['email1']
        ic.notes = bic['notes']
        if bic['phone2']:
            ic.alt_phones = [bic['phone2']]
        if bic['email3']:
            ic.alt_emails = [bic['email2'], bic['email3']]
        elif bic['email2']:
            ic.alt_emails = [bic['email2']]
        ic.owner_id = company.id
        ic.owner_name = company.name

        await es[IDX_INSURANCE_COMPANY].replace_one({'_id': ObjectId(ic.id)}, Payload.to_obj(ic), upsert=True)
