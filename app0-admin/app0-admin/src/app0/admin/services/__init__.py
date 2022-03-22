"""
Services module
"""
IDX_USER = 'app0.user'
IDX_APP = 'app0.app'
IDX_GROUP = 'app0.group'
IDX_ROLE = 'app0.role'
IDX_USER_ROLE = 'app0.user_role'
IDX_NOTIFICATION = 'app0.notification'
IDX_TEMPLATE_MAIL = 'app0.template_mail'
IDX_REGISTRATION = 'app0.registration'

# roles
ROLE_ADMIN = "app0_admin"
ROLE_USER = "app0_user"

# clients & claims db collections
IDX_EMPLOYEE = 'app0.employee'
IDX_PROVIDER = 'app0.provider'
IDX_CLIENT = 'app0.client'
IDX_CLAIM = 'app0.claim'

# user actions
ACT_USER_CREATE = "ACT_USER_CREATE"
ACT_USER_DELETE_USER = "ACT_USER_DELETE_USER"

# company actions
ACT_COMPANY_UPDATE_TMAILS = "ACT_COMPANY_UPDATE_TMAILS"
ACT_COMPANY_UPDATE_INS_COMPANIES = "ACT_COMPANY_UPDATE_INS_COMPANIES"
ACT_COMPANY_UPDATE_DAMAGES = "ACT_COMPANY_UPDATE_DAMAGES"
ACT_COMPANY_DELETE = "ACT_COMPANY_DELETE"

# registration actions
ACT_REGISTRATION_DELETE = "ACT_REGISTRATION_DELETE"

# plan actions
ACT_PLAN_DELETE = "ACT_PLAN_DELETE"

__all__ = ['user_services']