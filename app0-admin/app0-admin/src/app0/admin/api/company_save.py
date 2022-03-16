"""
Platform Company: company-save
"""
import os
from typing import Optional, Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.dataobjects.payload import Payload

from app0.admin.company import Company
from app0.admin.damage import Damage
from app0.admin.tmail import Tmail
from app0.admin.insurance import InsuranceCompany
from app0.admin.db import db
from app0.admin.enums import Enum, config_path
from app0.admin.http import HttpRespInfo
from app0.admin.services import (ACT_COMPANY_DELETE, ACT_COMPANY_UPDATE_DAMAGES, ACT_COMPANY_UPDATE_INS_COMPANIES,
                                  ACT_COMPANY_UPDATE_TMAILS, IDX_CLAIM, IDX_CLIENT, IDX_CLIENT_PROPERTY, IDX_COMPANY,
                                  IDX_COMPANY_MAIL, IDX_DAMAGE, IDX_EMPLOYEE, IDX_EVENT, IDX_INSURANCE_COMPANY,
                                  IDX_INSURANCE_EMPLOYEE, IDX_NOTIFICATION, IDX_PROVIDER, IDX_REGISTRATION,
                                  IDX_SUBSCRIPTION, IDX_USER, ROLE_ADMIN, IDX_COMPANY_CONFIG)
from app0.admin.services.company_services import save_company

BaseDamages = Enum.load_csv(config_path, "BaseDamages", '*')
BaseInsuranceCompanies = Enum.load_csv(config_path, "BaseInsuranceCompanies", '*')
BaseMails = Enum.load_csv(config_path, "BaseMails", '*')
TEMPLATES_FOLDER: Optional[str] = None

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(Company, "Company Info"),
    responses={
        200: (Company, "Company updated"),
        400: (str, "Request error"),
        403: (str, "Operation forbidden"),
    }
)


async def __init_event__(context: EventContext):
    global TEMPLATES_FOLDER
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])


async def run(payload: Company, context: EventContext, action: Optional[str] = None) -> Union[Company, HttpRespInfo]:
    """
    Company save actions
    """
    es = db(context.env)
    # check user admin
    if ROLE_ADMIN not in context.auth_info['payload'].get('roles', 'noauth'):
        return HttpRespInfo(403, 'User is not admin')

    if not action:
        await save_company(es, payload)
    elif action == ACT_COMPANY_UPDATE_TMAILS:
        await _update_tmails(es, payload)
    elif action == ACT_COMPANY_UPDATE_INS_COMPANIES:
        await _update_ins_companies(es, payload)
    elif action == ACT_COMPANY_UPDATE_DAMAGES:
        await _update_damages(es, payload)
    elif action == ACT_COMPANY_DELETE:
        await _company_delete(es, payload)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[Company, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[Company, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _company_delete(es, company: Company):
    """
    Delete Company and related info
    """
    await es[IDX_DAMAGE].delete_many({'owner_id': company.id})
    await es[IDX_EMPLOYEE].delete_many({'owner_id': company.id})
    await es[IDX_USER].delete_many({'owner_id': company.id})
    await es[IDX_EVENT].delete_many({'owner_id': company.id})
    await es[IDX_INSURANCE_COMPANY].delete_many({'owner_id': company.id})
    await es[IDX_INSURANCE_EMPLOYEE].delete_many({'owner_id': company.id})
    await es[IDX_PROVIDER].delete_many({'owner_id': company.id})
    await es[IDX_CLIENT].delete_many({'owner_id': company.id})
    await es[IDX_CLAIM].delete_many({'owner_id': company.id})
    await es[IDX_CLIENT_PROPERTY].delete_many({'owner_id': company.id})
    await es[IDX_NOTIFICATION].delete_many({'owner_id': company.id})
    await es[IDX_COMPANY_MAIL].delete_many({'owner_id': company.id})
    await es[IDX_COMPANY_CONFIG].delete_many({'owner_id': company.id})
    await es[IDX_REGISTRATION].delete_many({'company_id': company.id})
    await es[IDX_SUBSCRIPTION].delete_many({'company_id': company.id})
    await es[IDX_COMPANY].delete_one({'_id': ObjectId(company.id)})


async def _update_tmails(es, company: Company):
    """
    Process emails
    """
    for d in BaseMails:
        did = d['id']
        email = Tmail(
            name=d['name'],
            subject=d['subject'],
            template=d['template'],
            description=d['description'],
            tags=[d['tag']])
        doc = await es[IDX_COMPANY_MAIL].find_one({'$and': [{'name': {'$eq': d.name}},
                                                            {'owner_id': {'$eq': company.id}}]})
        if not doc:
            email.content = await _load_mail_base_content(did)
            assert company.id
            email.owner_id = company.id
            await es[IDX_COMPANY_MAIL].replace_one({'_id': ObjectId(email.id)}, Payload.to_obj(email), upsert=True)


async def _load_mail_base_content(did):
    assert TEMPLATES_FOLDER
    file_path = os.path.join(TEMPLATES_FOLDER, did + '_base_content.txt')
    if os.path.isfile(file_path):
        file = open(file_path, "r", encoding='utf8')
        cont = file.read()
        file.close()
        return cont
    return ''


async def _update_damages(es, company: Company):
    """
    Process damages
    """
    damages = [Damage(name=d['name'], category=d['category']) for d in BaseDamages]
    for d in damages:
        doc = await es[IDX_DAMAGE].find_one({'$and': [{'name': {'$eq': d.name}},
                                                      {'owner_id': {'$eq': company.id}}]})

        if not doc:
            d.owner_id = company.id
            await es[IDX_DAMAGE].replace_one({'_id': ObjectId(d.id)}, Payload.to_obj(d), upsert=True)


async def _update_ins_companies(es, company: Company):
    """
    Process Insurance Companies
    """
    for d in BaseInsuranceCompanies:
        ic = InsuranceCompany(name=d['name'])
        ic.address = d['address']
        ic.aptsuiteunit = d['aptsuiteunit']
        ic.city = d['city']
        ic.state = d['state']
        ic.zipcode = d['zipcode']
        ic.phone_number = d['phone1']
        ic.email = d['email1']
        ic.notes = d['notes']
        if d['phone2']:
            ic.alt_phones = [d['phone2']]
        if d['email3']:
            ic.alt_emails = [d['email2'], d['email3']]
        elif d['email2']:
            ic.alt_emails = [d['email2']]
        ic.owner_id = company.id

        doc = await es[IDX_INSURANCE_COMPANY].find_one({'$and': [{'name': {'$eq': ic.name}},
                                                                 {'owner_id': {'$eq': company.id}}]})
        if not doc:
            await es[IDX_INSURANCE_COMPANY].replace_one({'_id': ObjectId(ic.id)},
                                                        Payload.to_obj(ic),
                                                        upsert=True)
