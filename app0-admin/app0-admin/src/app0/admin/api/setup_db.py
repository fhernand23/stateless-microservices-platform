"""
Platform Setup: setup-db
"""
import os
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.fs_storage import FileStorage

from app0.admin.app import AppDef, AppRole
from app0.admin.db import db
from app0.admin.http import Dto, HttpRespInfo
from app0.admin.services import (IDX_APP, IDX_GROUP, IDX_NOTIFICATION, IDX_REGISTRATION, IDX_ROLE, IDX_TEMPLATE_MAIL,
                                 IDX_USER, IDX_USER_ROLE, IDX_CLAIM, IDX_CLIENT, IDX_EMPLOYEE, IDX_PROVIDER,
                                 ROLE_USER, ROLE_ADMIN)
from app0.admin.services.app_services import save_app, save_role
from app0.admin.services.template_mail_services import save_template_mail
from app0.admin.services.user_services import save_user, save_user_role
from app0.admin.template_mail import TemplateMail
from app0.admin.user import User, UserAppRole
from app0.platform.auth import UserPassword, _password_hash

logger = app_logger()
fs_auth: Optional[FileStorage] = None
DEF_SUPERADMIN_USERNAME = "superuser"
DEF_PASSWORD = "123"
DEF_ROLES = [ROLE_USER]
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
    global fs_auth, TEMPLATES_FOLDER
    if fs_auth is None:
        fs_auth = FileStorage(path=str(context.env['fs']['auth_store']))
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
        req_colls = [IDX_APP, IDX_GROUP, IDX_NOTIFICATION, IDX_REGISTRATION, IDX_ROLE, IDX_USER,
                     IDX_USER_ROLE, IDX_CLAIM, IDX_CLIENT, IDX_EMPLOYEE, IDX_PROVIDER, IDX_TEMPLATE_MAIL]
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
                    email="superuser@app0")
        await save_user(es, user)
        print(f"user saved: {DEF_SUPERADMIN_USERNAME}")
        await _register(DEF_SUPERADMIN_USERNAME, DEF_PASSWORD)
        print(f"password hashed: {DEF_SUPERADMIN_USERNAME}")

        await _create_user_roles(es, DEF_SUPERADMIN_USERNAME, ROLE_USER)
        await _create_user_roles(es, DEF_SUPERADMIN_USERNAME, ROLE_ADMIN)

        # create email base templates
        await _create_email_templates(es)

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
    role1 = AppRole(name=ROLE_USER, description="App0 User")
    await save_role(es, role1)
    print(f"saved role: {ROLE_USER}")
    role2 = AppRole(name=ROLE_ADMIN, description="App0 Admin")
    await save_role(es, role2)
    print(f"saved role: {ROLE_ADMIN}")

    # create app
    app_claims = AppDef(
        name="App0 Claims",
        description="App0 Claims Management",
        url='',
        default_role=ROLE_USER)
    await save_app(es, app_claims)
    print("saved app: app_claims")
    app_clients = AppDef(
        name="App0 Clients",
        description="App0 Clients Management",
        url='',
        default_role=ROLE_USER)
    await save_app(es, app_clients)
    print("saved app: app_clients")


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
        TemplateMail(
            name="email_confirmation",
            subject="Verify your email address",
            template="email-confirmation.html"),
        TemplateMail(
            name="welcome",
            subject="Welcome to Claims Attendant",
            template="welcome.html"),
        TemplateMail(
            name="password_reset",
            subject="Reset your Claims Attendant password",
            template="password-reset.html"),
        TemplateMail(
            name="password_reset_ok",
            subject="Claims Attendant password succesfully changed",
            template="password-reset-ok.html"),
    ]
    for d in emails:
        await save_template_mail(es, d)
        print(f"saved {d.name}")


async def _load_mail_base_content(did):
    assert TEMPLATES_FOLDER
    file_path = os.path.join(TEMPLATES_FOLDER, did + '_base_content.txt')
    if os.path.isfile(file_path):
        file = open(file_path, "r", encoding="utf-8")
        cont = file.read()
        file.close()
        return cont
    return ''
