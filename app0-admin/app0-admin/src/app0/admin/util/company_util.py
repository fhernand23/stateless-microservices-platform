"""
module: company_util
"""
from typing import Tuple
from app0.admin.common import IdDescriptionField, IdDescription


SYSTEM_USER = "system"
SYSTEM_USER_DESC = "System"
APP_BASE = "app0-admin"
APP_ATTENDANT = "claims-attendant"

# this values are also in employee-team & option.ts in UI. Should be put in Config collection
POSITION_OP_MANAGER = IdDescription("operations_manager", "Operations Manager")
POSITION_ADJUSTER = IdDescription("adjuster", "Adjuster")
POSITION_ASSISTANT = IdDescription("pa_assistant_desk_ajuster", "PA Assistant/Desk Adjuster")

TEAM_ADJUSTERS = IdDescription('adjusters', 'Adjusters')
TEAM_MANAGERS = IdDescription('managers', 'Managers')
TEAM_ASSISTANTS = IdDescription('assistants', 'Assistants')

PROVIDER_ESTIMATOR = IdDescription('estimator', 'Estimator')
PROVIDER_APPRAISER = IdDescription('appraiser', 'Appraiser')
PROVIDER_UMPIRE = IdDescription('umpire', 'Umpire')
PROVIDER_ATTORNEY = IdDescription('attorney', 'Attorney')

EVENT_FIRST_INSPECTION = IdDescription('first_inspection', 'First Inspection')
EVENT_RE_INSPECTION = IdDescription('re_inspection', 'Re Inspection')
EVENT_SPECIALIZED_INSPECTION = IdDescription('specialized_inspection', 'Specialized Inspection')

EVENT_REPR_COMPANY = 'In-House Adjuster'
EVENT_REPR_INS_COMPANY = 'Company Adjuster'
EVENT_REPR_PROVIDER = 'Service Provider'
EVENT_REPR_OTHER = 'Other'

OBJECT_COMPANY = "Company"
OBJECT_CLAIM = "Claim"

TYPE_LOG = "log"
TYPE_DIRECT = "direct"
TYPE_UPLOAD = "upload"

file_types = [
    IdDescriptionField('W9', 'W9 document', 'w9_document_date', 'w9_document_resource'),
    IdDescriptionField('ATTORNEY_LIST', 'Attorney List', 'attorney_list_date', 'attorney_list_resource'),
    IdDescriptionField('-', 'File', ''),
]


def get_file_description(val) -> str:
    """get label"""
    fts = [ft for ft in file_types if ft.value == val]
    if fts and len(fts) > 0:
        return fts[0].label
    return ''


def get_file_field_date(val) -> str:
    """get field in claim"""
    fts = [ft for ft in file_types if ft.value == val]
    if fts and len(fts) > 0:
        return fts[0].fld_name_date
    return ''


def get_file_field_date_resource(val) -> Tuple[str, str]:
    """get field in claim"""
    fts = [ft for ft in file_types if ft.value == val]
    if fts and len(fts) > 0:
        return fts[0].fld_name_date, fts[0].fld_name_resource
    return '', ''
