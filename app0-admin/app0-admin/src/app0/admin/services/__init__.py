"""
Services module
"""
IDX_USER = 'app0.user'
IDX_APP = 'app0.app'
IDX_GROUP = 'app0.group'
IDX_ROLE = 'app0.role'
IDX_USER_ROLE = 'app0.user_role'
IDX_NOTIFICATION = 'app0.notification'
IDX_BASE_MAIL = 'app0.tmail'
IDX_REGISTRATION = 'app0.registration'
IDX_PLAN = 'app0.plan'

# roles
ROLE_ADMIN = "App0 Admin"
ROLE_USER = "App0 User"

# clients & claims db collections
IDX_EMPLOYEE = 'app0.employee'
IDX_PROVIDER = 'app0.provider'
IDX_CLIENT = 'app0.client'
IDX_CLAIM = 'app0.claim'

# user actions
ACT_USER_CREATE = "ACT_USER_CREATE"
ACT_USER_DELETE_USER = "ACT_USER_DELETE_USER"

# registration actions
ACT_REGISTRATION_DELETE = "ACT_REGISTRATION_DELETE"

# plan actions
ACT_PLAN_DELETE = "ACT_PLAN_DELETE"

# role actions
ACT_ROLE_ARCHIVE = "ACT_ROLE_ARCHIVE"
ACT_ROLE_UNARCHIVE = "ACT_ROLE_UNARCHIVE"

# app actions
ACT_APP_ARCHIVE = "ACT_APP_ARCHIVE"
ACT_APP_UNARCHIVE = "ACT_APP_UNARCHIVE"

# user-role actions
ACT_USERROLE_DELETE = "ACT_USERROLE_DELETE"

__all__ = ['user_services']
