"""
Platform Setup: setup-db
"""
import os
from datetime import datetime, timezone
from typing import List, Optional, Union
from decimal import Decimal

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.fs_storage import FileStorage
from hopeit.dataobjects.payload import Payload

from app0.admin.app import AppDef, AppRole
from app0.admin.company import Company, CompanyConfig
from app0.admin.db import db
from app0.admin.http import Dto, HttpRespInfo
from app0.admin.notification import Notification
from app0.admin.services import (IDX_APP, IDX_COMPANY, IDX_COMPANY_CONFIG, IDX_EVENT, IDX_GROUP, IDX_NOTIFICATION,
                                  IDX_PLAN, IDX_REGISTRATION, IDX_ROLE, IDX_SUBSCRIPTION, IDX_BASE_MAIL, IDX_USER,
                                  IDX_USER_ROLE, IDX_CLAIM, IDX_CLIENT, IDX_CLIENT_PROPERTY, IDX_DAMAGE, IDX_EMPLOYEE,
                                  IDX_INSURANCE_COMPANY, IDX_INSURANCE_EMPLOYEE, IDX_PROPERTY, IDX_PROVIDER,
                                  IDX_COMPANY_MAIL, IDX_TOKEN, ROLE_USER, ROLE_ADMIN,
                                  ROLE_COMPANY_ADMIN, ROLE_USER_PROVIDER)
from app0.admin.util.company_util import (TEAM_ADJUSTERS, TEAM_MANAGERS, TEAM_ASSISTANTS, POSITION_OP_MANAGER,
                                           POSITION_ADJUSTER, POSITION_ASSISTANT, PROVIDER_ESTIMATOR,
                                           PROVIDER_ATTORNEY, PROVIDER_APPRAISER, PROVIDER_UMPIRE)
from app0.admin.services.app_services import save_app, save_role
from app0.admin.services.company_services import save_company
from app0.admin.services.tmail_services import save_tmail
from app0.admin.services.plan_services import save_plan
from app0.admin.services.user_services import save_user, save_user_role
from app0.admin.tmail import Tmail
from app0.admin.registration import Registration
from app0.admin.provider import Provider
from app0.admin.user import User, UserAppRole
from app0.platform.auth import UserPassword, _password_hash
from app0.admin.util import company_util
from app0.admin.services.registration_services import save_registration
from app0.admin.subscription import BillingInfo, Subscription, PlanInfo
from app0.admin.employee import Employee
from app0.admin.enums import Enum, config_path
from app0.admin.subscription import AvailablePlan
from app0.admin.insurance import InsuranceCompany
from app0.admin.damage import Damage

logger = app_logger()
fs_auth: Optional[FileStorage] = None
ATTENDANT_URL: Optional[str] = None
DEF_SUPERADMIN_USERNAME = "superuser"
DEF_PASSWORD = "123"
DEF_ROLES = [ROLE_COMPANY_ADMIN, ROLE_USER]
BaseDamages = Enum.load_csv(config_path, "BaseDamages", '*')
BaseInsuranceCompanies = Enum.load_csv(config_path, "BaseInsuranceCompanies", '*')
BaseMails = Enum.load_csv(config_path, "BaseMails", '*')
TEMPLATES_FOLDER: Optional[str] = None

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('code', str, "Setup Code")
    ],
    responses={
        200: (Dto, "OK"),
        400: (str, "Bad request"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def __init_event__(context: EventContext):
    global fs_auth, ATTENDANT_URL, TEMPLATES_FOLDER
    if fs_auth is None:
        fs_auth = FileStorage(path=str(context.env['fs']['auth_store']))
    if ATTENDANT_URL is None:
        ATTENDANT_URL = str(context.env["env_config"]["claimsattendant_url"])
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])


async def run(payload: None, context: EventContext, code: str) -> Union[Dto, HttpRespInfo]:
    """
    Initialize DB
    """
    # check if empty
    if code == 'FORCE':
        es = db(context.env)
        # check if collections exists and create or clean
        query = {"name": {"$regex": r"^(?!system\.)"}}
        req_colls = [IDX_APP, IDX_COMPANY, IDX_COMPANY_CONFIG, IDX_EVENT, IDX_GROUP, IDX_NOTIFICATION,
                     IDX_PLAN, IDX_REGISTRATION, IDX_ROLE, IDX_SUBSCRIPTION, IDX_BASE_MAIL, IDX_USER,
                     IDX_USER_ROLE, IDX_CLAIM, IDX_CLIENT, IDX_CLIENT_PROPERTY, IDX_DAMAGE, IDX_EMPLOYEE,
                     IDX_INSURANCE_COMPANY, IDX_INSURANCE_EMPLOYEE, IDX_PROPERTY, IDX_PROVIDER,
                     IDX_COMPANY_MAIL, IDX_TOKEN]
        coll_names = await es.list_collection_names(filter=query)
        print(f"coll existentes: {coll_names}")
        for col in req_colls:
            if col in coll_names:
                await es.drop_collection(col)
                print(f"coll {col} dropped")
            await es.create_collection(col)
            print(f"coll {col} created")
        # create base Apps & Roles
        await _create_base_apps_roles(es)

        # create superadmin user
        user = User(firstname="Superuser",
                    surname="Admin",
                    username=DEF_SUPERADMIN_USERNAME,
                    email="superuser@claims")
        await save_user(es, user)
        print(f"user saved: {DEF_SUPERADMIN_USERNAME}")
        await _register(DEF_SUPERADMIN_USERNAME, DEF_PASSWORD)
        print(f"password hashed: {DEF_SUPERADMIN_USERNAME}")

        await _create_user_roles(es, DEF_SUPERADMIN_USERNAME, ROLE_USER)
        await _create_user_roles(es, DEF_SUPERADMIN_USERNAME, ROLE_ADMIN)

        # create email base templates
        await _create_email_templates(es)

        # create plans
        plans = await _create_plans(es)

        # create registration
        assert plans[0].id
        registration = Registration(
            firstname="James", surname="TheOwner", email="james@company", phone="+13054428710",
            position=POSITION_OP_MANAGER,
            address="5050 W Flagler St, Miami, FL 33134, Estados Unidos",
            company_name="Company1", company_phone="+13054428710",
            company_address="5050 W Flagler St, Miami, FL 33134, Estados Unidos",
            company_email="info@company", plan_id=plans[0].id, plan_name=plans[0].name,
            plan_description=plans[0].description, plan_annual_payment=plans[0].annual_payment,
            plan_monthly_amount=plans[0].monthly_amount, plan_max_open_claims=plans[0].max_open_claims,
            plan_max_adjusters=plans[0].max_adjusters, creation_date=datetime.now(tz=timezone.utc))
        await save_registration(es, registration)

        company = Company(
            name=registration.company_name, address=registration.company_address,
            phone_number=registration.company_phone, email=registration.company_email)
        await _create_company(es, company)

        # create user & employee
        employee = Employee(
            firstname=registration.firstname, surname=registration.surname, email=registration.email,
            phone_number=registration.phone, position=registration.position,
            teams=[TEAM_ADJUSTERS, TEAM_MANAGERS], address=registration.address,
            owner_id=company.id, owner_name=company.name, company_representative=True,
            public_adjuster_license=True, license_id="lic789456")
        user = await _create_employee(es, employee, DEF_ROLES)
        # create susbscription
        await _create_subscription(es, registration, company, user)

        # create base data
        await _create_tmails(es, company)
        await _create_damages(es, company)
        await _create_ins_companies(es, company)

        assert company.id
        registration.company_id = company.id
        registration.status = 'Confirmed'
        registration.confirm_date = datetime.now(tz=timezone.utc)
        await save_registration(es, registration)
        await _create_employees(es, company)
        await _create_providers(es, company)

    return Dto(o={'msg': 'OK Run'})


async def __postprocess__(payload: Union[Dto, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[Dto, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _register(username: str, password: str) -> bool:
    """
    Register User and password
    """
    if fs_auth is None:
        return False
    auth_info = await fs_auth.get(key=username, datatype=UserPassword)

    if auth_info is not None:
        # exists user
        return False

    # register password
    await fs_auth.store(key=username, value=_password_hash(password))  # Improve process
    return True


async def _create_base_apps_roles(es):
    """
    Create Base Roles & Apps
    """
    # ROLE_USER,ROLE_ADMIN,ROLE_COMPANY_ADMIN,ROLE_USER_PROVIDER
    role1 = AppRole(name=ROLE_USER, description="Claims Attendant User")
    await save_role(es, role1)
    print(f"saved role: {ROLE_USER}")
    role2 = AppRole(name=ROLE_ADMIN, description="Claims Platform Admin")
    await save_role(es, role2)
    print(f"saved role: {ROLE_ADMIN}")
    role3 = AppRole(name=ROLE_COMPANY_ADMIN, description="Claims Attendant Company Admin")
    await save_role(es, role3)
    print(f"saved role: {ROLE_COMPANY_ADMIN}")
    role4 = AppRole(name=ROLE_USER_PROVIDER, description="Claims Attendant Service Provider")
    await save_role(es, role4)
    print(f"saved role: {ROLE_USER_PROVIDER}")

    # create app
    app_attendant = AppDef(name="claims-attendant",
                           description="Claims Attendant",
                           url=ATTENDANT_URL,
                           image="/claims/images/apps/claims_attendant.png",
                           default_role=ROLE_USER)
    await save_app(es, app_attendant)
    print("saved app: attendant")


async def _create_user_roles(es, username: str, rolename: str):
    """
    Create User Roles
    """
    ur = UserAppRole(username, rolename)
    await save_user_role(es, ur)
    print(f"saved user role: {ur}")


async def _create_email_templates(es):
    """Create Email Templates"""
    emails = [
        Tmail(name="email_confirmation", subject="Verify your email address", template="email-confirmation.html"),
        Tmail(name="welcome", subject="Welcome to Claims Attendant", template="welcome.html"),
        Tmail(name="password_reset", subject="Reset your Claims Attendant password", template="password-reset.html"),
        Tmail(name="password_reset_ok", subject="Claims Attendant password succesfully changed",
              template="password-reset-ok.html"),
    ]
    for d in emails:
        await save_tmail(es, d)
        print(f"saved {d.name}")


async def _create_plans(es) -> List[AvailablePlan]:
    """Create plans"""
    plans = [
        AvailablePlan(
            name="Professionals", subtitle="Plan for professionals", annual_payment=True,
            monthly_amount=Decimal(125), annual_amount=Decimal(1250), max_open_claims=0, max_adjusters=3,
            max_storage=250),
    ]
    for d in plans:
        await save_plan(es, d)
        print(f"saved {d.name}")

    return plans


async def _create_company(es, company: Company):
    """
    Create Company
    """
    await save_company(es, company)
    company_config = CompanyConfig(owner_id=company.id, owner_name=company.name)
    await es[IDX_COMPANY_CONFIG].replace_one({'_id': ObjectId(company_config.id)},
                                             Payload.to_obj(company_config),
                                             upsert=True)
    # create notifications
    await _create_notification_company(es, company)


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


async def _create_employee(es, employee: Employee, roles: List[str]) -> User:
    """
    Create employee
    """
    await es[IDX_EMPLOYEE].replace_one({'_id': ObjectId(employee.id)}, Payload.to_obj(employee), upsert=True)
    # create user
    user = User(firstname=employee.firstname, surname=employee.surname, username=employee.email,
                email=employee.email, phone_number=employee.phone_number, owner_id=employee.owner_id,
                owner_name=employee.owner_name, employee_id=employee.id,
                company_representative=employee.company_representative)
    await es[IDX_USER].replace_one({'_id': ObjectId(user.id)}, Payload.to_obj(user), upsert=True)
    # set user roles
    for role in roles:
        user_app_role = UserAppRole(user.username, role)
        await es[IDX_USER_ROLE].replace_one({'_id': ObjectId(user_app_role.id)},
                                            Payload.to_obj(user_app_role), upsert=True)
    # generate token to set password
    await _register(user.username, DEF_PASSWORD)
    # create notifications
    await _create_notification_user(es, user)
    print(f"saved {employee.email}")

    return user


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


async def _create_employees(es, company: Company):
    """Create some employees for company"""
    assert company.id
    employee1 = Employee(
        firstname="Mary", surname="TheAdjuster", email="mary@company",
        phone_number="+17862694265", position=POSITION_ADJUSTER,
        teams=[TEAM_ADJUSTERS], address="3610 NW 15th St, Miami, FL 33125, Estados Unidos",
        owner_id=company.id, owner_name=company.name, company_representative=False,
        public_adjuster_license=True, license_id="lic456321")
    await _create_employee(es, employee1, [ROLE_USER])
    employee2 = Employee(
        firstname="Jennifer", surname="TheAssistant", email="jennifer@company",
        phone_number="+13056068239", position=POSITION_ASSISTANT,
        teams=[TEAM_ASSISTANTS], address="1811 NW 36th Ave, Miami, FL 33125, Estados Unidos",
        owner_id=company.id, owner_name=company.name, company_representative=False,
        public_adjuster_license=False)
    await _create_employee(es, employee2, [ROLE_USER])


async def _create_providers(es, company: Company):
    """Create some providers for company"""
    assert company.id
    provider1 = Provider(
        firstname="Robert", surname="TheEstimator", email="robert@mail",
        phone_number="+13056068239", service_types=[PROVIDER_ESTIMATOR],
        address="1811 NW 36th Ave, Miami, FL 33125, Estados Unidos",
        owner_id=company.id, owner_name=company.name)
    await es[IDX_PROVIDER].replace_one({'_id': ObjectId(provider1.id)}, Payload.to_obj(provider1), upsert=True)
    provider2 = Provider(
        firstname="John", surname="TheAppraiser", email="john@mail",
        phone_number="+13056068239", service_types=[PROVIDER_APPRAISER],
        address="1811 NW 36th Ave, Miami, FL 33125, Estados Unidos",
        owner_id=company.id, owner_name=company.name)
    await es[IDX_PROVIDER].replace_one({'_id': ObjectId(provider2.id)}, Payload.to_obj(provider2), upsert=True)
    provider3 = Provider(
        firstname="Michael", surname="TheUmpire", email="michael@mail",
        phone_number="+13056068239", service_types=[PROVIDER_UMPIRE],
        address="1811 NW 36th Ave, Miami, FL 33125, Estados Unidos",
        owner_id=company.id, owner_name=company.name)
    await es[IDX_PROVIDER].replace_one({'_id': ObjectId(provider3.id)}, Payload.to_obj(provider3), upsert=True)
    provider4 = Provider(
        firstname="William", surname="TheAttorney", email="william@mail",
        phone_number="+13056068239", service_types=[PROVIDER_ATTORNEY],
        address="1811 NW 36th Ave, Miami, FL 33125, Estados Unidos",
        owner_id=company.id, owner_name=company.name)
    await es[IDX_PROVIDER].replace_one({'_id': ObjectId(provider4.id)}, Payload.to_obj(provider4), upsert=True)
