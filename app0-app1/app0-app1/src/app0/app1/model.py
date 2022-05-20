"""
App0Platform: Model
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.common import IdDescription

@dataobject
@dataclass
class ModelInput:
    """
    Model Input
    """
    inspection_date: datetime = fd("Creation date")
    inhouse_adjusters: List[IdDescription] = fd("In-house adjusters", default_factory=list)
    inscomp_representatives: List[IdDescription] = fd("Ins company representatives", default_factory=list)
    notes: str = fd("Notes", default='')


@dataobject
@dataclass
class ModelOutput:
    """
    Model Output
    """
    rel_upload_date: Optional[datetime] = fd("Release upload date", default=None)
    rel_client_files: List[IdDescription] = fd("Send Release to client files", default_factory=list)
    rel_client_dest: List[str] = fd("Send Release to client mails", default_factory=list)
    rel_client_dest2: List[str] = fd("Send Release to client mails2", default_factory=list)
    rel_send_client_date: Optional[datetime] = fd("Send Release to client date", default=None)
    rel_client_upload_date: Optional[datetime] = fd("Release received upload date", default=None)
    rel_client_approved: Optional[bool] = fd("Release received Approved", default=False)
    rel_client_approved_desc: Optional[str] = fd("Release received Approved description", default=None)
    rel_ic_files: List[IdDescription] = fd("Send Release mail to IC files", default_factory=list)
    rel_ic_dest: List[str] = fd("Send Release mail to IC mails", default_factory=list)
    rel_ic_dest2: List[str] = fd("Send Release mail to IC mails2", default_factory=list)
    rel_ic_date: Optional[datetime] = fd("Send Release to ins comp date", default=None)
    app_appraiser: Optional[IdDescription] = fd("Appraisal Appraiser", default=None)
    app_appraiser_date: Optional[datetime] = fd("Appraisal Appraiser date available", default=None)
    app_award_upload_date: Optional[datetime] = fd("Appraisal award upload date", default=None)
    app_icesti_upload_date: Optional[datetime] = fd("Appraisal ic estimate upload date", default=None)
    app_appr_files: List[IdDescription] = fd("Send Release mail to Appraiser files", default_factory=list)
    app_appr_dest: List[str] = fd("Send Release mail to Appraiser mails", default_factory=list)
    app_appr_dest2: List[str] = fd("Send Release mail to Appraiser mails2", default_factory=list)
    app_appr_date: Optional[datetime] = fd("Send Release to Appraiser date", default=None)
    ump_umpire: Optional[IdDescription] = fd("Umpire", default=None)
    ump_sou_upload_date: Optional[datetime] = fd("Appraisal award upload date", default=None)
    ump_ack_upload_date: Optional[datetime] = fd("Appraisal acknowledgment upload date", default=None)
    ump_ack_client_files: List[IdDescription] = fd("Send Ack to client files", default_factory=list)
    ump_ack_client_dest: List[str] = fd("Send Ack to client mails", default_factory=list)
    ump_ack_client_dest2: List[str] = fd("Send Ack to client mails2", default_factory=list)
    ump_ack_send_client_date: Optional[datetime] = fd("Send Ack to client date", default=None)
    ump_ack_cli_upload_date: Optional[datetime] = fd("Acknowledgment from client upload date", default=None)
    ump_ack_client_approved: Optional[bool] = fd("Acknowledgment from client Approved", default=False)
    ump_ack_client_approved_desc: Optional[str] = fd("Ack from client Approved description", default=None)
    ump_umpire_date: Optional[datetime] = fd("Umpire date available", default=None)
    ump_esx_request_est_date: Optional[datetime] = fd("Request ESX from estimator", default=None)
    ump_esx_upload_date: Optional[datetime] = fd("Umpire ESX upload date", default=None)
    ump_esx_files: List[IdDescription] = fd("Send ESX mail to Umpire files", default_factory=list)
    ump_esx_dest: List[str] = fd("Send ESX mail to Umpire mails", default_factory=list)
    ump_esx_dest2: List[str] = fd("Send ESX mail to Umpire mails2", default_factory=list)
    ump_esx_date: Optional[datetime] = fd("Send ESX to Umpire date", default=None)
    ump_award_upload_date: Optional[datetime] = fd("Umpire award upload date", default=None)
    ump_estimate_upload_date: Optional[datetime] = fd("Umpire estimate upload date", default=None)
    ump_invoice_upload_date: Optional[datetime] = fd("Umpire invoice upload date", default=None)
    ump_invoice: Optional[str] = fd("Pending payment/Payed", default=None)
    est_icesti_upload_date: Optional[datetime] = fd("Estimate ic estimate upload date", default=None)
    agr_emproof_upload_date: Optional[datetime] = fd("Agreement email proof upload date", default=None)
    agr_icesti_upload_date: Optional[datetime] = fd("Agreement ic estimate upload date", default=None)
    att_reason: Optional[str] = fd("Attorney reason", default=None)
    att_attorney: Optional[IdDescription] = fd("Attorney", default=None)
    att_ret_client_dest: List[str] = fd("Send Retainer to client mails", default_factory=list)
    att_ret_client_dest2: List[str] = fd("Send Retainer to client mails2", default_factory=list)
    att_ret_send_client_date: Optional[datetime] = fd("Send Retainer to client date", default=None)
    att_ret_cli_upload_date: Optional[datetime] = fd("Retainer from client upload date", default=None)
    att_ret_client_approved: Optional[bool] = fd("Retainer from client Approved", default=False)
    att_ret_client_approved_desc: Optional[str] = fd("Retainer from client Approved description", default=None)
    att_ret_files: List[IdDescription] = fd("Send Retainer mail to Attorney files", default_factory=list)
    att_ret_dest: List[str] = fd("Send Retainer mail to Attorney mails", default_factory=list)
    att_ret_dest2: List[str] = fd("Send Retainer mail to Attorney mails2", default_factory=list)
    att_ret_date: Optional[datetime] = fd("Send Retainer to Attorney date", default=None)
    amount: Optional[Decimal] = fd("Amount $", default=None)
    notes: Optional[str] = fd("Resolution notes", default=None)
    claim_resolved: Optional[bool] = fd("Claim Resolved", default=False)
    payment_regularized: Optional[bool] = fd("Payment Regularized", default=False)


@dataobject
@dataclass
class ModelRun:
    """
    Model Run
    """
    property_address: str = fd("Property address")
    claim_type: str = fd("New, Reopen or Emergency")
    public_adjuster: IdDescription = fd("Public adjuster")
    insurance_company: IdDescription = fd("Insurance Company")
    property_type: str = fd("Property type")
    creation_date: datetime = fd("Creation date")
    loss_date: datetime = fd("Date of loss")
    clients: List[IdDescription] = fd("Clients", default_factory=list)
    damage: IdDescription = fd("Damage type", default=None)
    file_number: str = fd("Internal App0 App1 File Number", default='')
    claim_number: str = fd("Insurance Company Claim Number", default='')
    apprentice: Optional[IdDescription] = fd("Apprentice (if applicable)", default=None)
    policy_number: Optional[str] = fd("Policy number", default='')
    deductible_amount: Decimal = fd("Deductible Amount $", default=Decimal("0.00"))
    spanish_only: bool = fd("Spanish only speaker", default=False)
    water_limit: bool = fd("10k water limit", default=False)
    mold: bool = fd("Mold", default=False)
    mold_limit: Optional[Decimal] = fd("Mold limit $ (if mold)", default=None)
    mitigation: bool = fd("Mitigation", default=False)
    tarp: bool = fd("Tarp", default=False)
    mortgage: bool = fd("Mortgage", default=False)
    mortgage_lender: Optional[str] = fd("Mortgage lender", default=None)
    mortgage_behind_payment: bool = fd("Mortgage behind payment", default=False)
    mortgage_process_of_loan_modification: bool = fd("Mortgage process of loan modification", default=False)
    mortgage_property_in_foreclosure: bool = fd("Mortgage property in foreclosure", default=False)
    rental: bool = fd("Rental property", default=False)
    rental_tenant_name: Optional[str] = fd("Rental tenant name", default=None)
    rental_tenant_phone: Optional[str] = fd("Rental tenant phone", default=None)
    rental_tenant_email: Optional[str] = fd("Rental tenant email", default=None)
    loss_description: str = fd("Loss description", default='')
    loss_repairs_done: bool = fd("Loss repairs done?", default=False)
    loss_pictures: bool = fd("Loss pictures?", default=True)
    loss_damage_type: str = fd("Loss repairs done?", default='')
    loss_roof_type: str = fd("Loss roof type", default='')
    loss_roof_material: str = fd("Loss roof material", default='')
    loss_roof_tile_type: str = fd("Loss roof tile type", default='')
    property_geometry: Optional[AddressGeoJson] = fd("Geo JSON Coordinates", default=None)
    property_address_zip: Optional[str] = fd("Zip Code", default=None)
    owner_id: Optional[str] = fd("Owner Id", default=None)
    owner_name: Optional[str] = fd("Owner Name", default=None)
    open_lor_upload_date: Optional[datetime] = fd("LOR upload date", default=None)
    open_scope_upload_date: Optional[datetime] = fd("SCOPE upload date", default=None)
    open_dec_upload_date: Optional[datetime] = fd("DEC upload date", default=None)
    open_other_upload_date: Optional[datetime] = fd("OTHER REQ upload date", default=None)
    open_lor_ic_files: List[IdDescription] = fd("Send LOR mail to IC files", default_factory=list)
    open_lor_ic_dest: List[str] = fd("Send LOR mail to IC mails", default_factory=list)
    open_lor_ic_dest2: List[str] = fd("Send LOR mail to IC mails2", default_factory=list)
    open_lor_ic_date: Optional[datetime] = fd("Send LOR mail to IC date", default=None)
    estimator: Optional[IdDescription] = fd("Estimator", default=None)
    open_estimator_dest2: List[str] = fd("Send Claim mail to estimator mails2", default_factory=list)
    open_estimator_date: Optional[datetime] = fd("Send Claim mail to estimator date", default=None)
    inspection_1: Optional[ClaimInspection] = fd("First Inspection", default=None)
    inspection_2: Optional[ClaimInspection] = fd("Second Inspection", default=None)
    inspection_3: Optional[ClaimInspection] = fd("Specialized Inspection", default=None)
    mitigation_benefit_upload_date: Optional[datetime] = fd("Benefit upload date", default=None)
    mitigation_invoice_upload_date: Optional[datetime] = fd("Invoice upload date", default=None)
    mitigation_photo_upload_date: Optional[datetime] = fd("Photo upload date", default=None)
    mitigation_docs_ic_files: List[IdDescription] = fd("Send Mitigation mail to IC files", default_factory=list)
    mitigation_docs_ic_dest: List[str] = fd("Send Mitigation mail to IC mails", default_factory=list)
    mitigation_docs_ic_dest2: List[str] = fd("Send Mitigation mail to IC mails2", default_factory=list)
    mitigation_docs_ic_date: Optional[datetime] = fd("Send Mitigation mail to IC date", default=None)
    receipts_upload_date: Optional[datetime] = fd("Receipts upload date", default=None)
    receipts_invoice_upload_date: Optional[datetime] = fd("Receipts invoices upload date", default=None)
    receipts_docs_ic_files: List[IdDescription] = fd("Send Receipts mail to IC files", default_factory=list)
    receipts_docs_ic_dest: List[str] = fd("Send Receipts mail to IC mails", default_factory=list)
    receipts_docs_ic_dest2: List[str] = fd("Send Receipts mail to IC mails2", default_factory=list)
    receipts_docs_ic_date: Optional[datetime] = fd("Send Receipts mail to IC date", default=None)
    receive_estimation_date: Optional[datetime] = fd("Date of receiving estimate from estimator", default=None)
    estimate_upload_date: Optional[datetime] = fd("Estimate upload date", default=None)
    estimate_amount: Optional[Decimal] = fd("Estimate Amount $", default=None)
    estimate_docs_ic_files: List[IdDescription] = fd("Send Receipts mail to IC files", default_factory=list)
    estimate_docs_ic_dest: List[str] = fd("Send Receipts mail to IC mails", default_factory=list)
    estimate_docs_ic_dest2: List[str] = fd("Send Receipts mail to IC mails2", default_factory=list)
    estimate_docs_ic_date: Optional[datetime] = fd("Send Estimate mail to IC date", default=None)
    spol_client_files: List[IdDescription] = fd("Send SPOL unsigned mail to client files", default_factory=list)
    spol_client_dest: List[str] = fd("Send SPOL unsigned mail to client mails", default_factory=list)
    spol_client_dest2: List[str] = fd("Send SPOL unsigned mail to client mails2", default_factory=list)
    spol_send_client_date: Optional[datetime] = fd("Send SPOL to client", default=None)
    spol_unsigned_upload_date: Optional[datetime] = fd("SPOL Unsigned by client upload date", default=None)
    spol_upload_date: Optional[datetime] = fd("SPOL Signed by client upload date", default=None)
    spol_client_approved: Optional[bool] = fd("SPOL Approved", default=False)
    spol_client_approved_desc: Optional[str] = fd("SPOL Approved description", default=None)
    spol_ic_files: List[IdDescription] = fd("Send SPOL mail to IC files", default_factory=list)
    spol_ic_dest: List[str] = fd("Send SPOL mail to IC mails", default_factory=list)
    spol_ic_dest2: List[str] = fd("Send SPOL mail to IC mails2", default_factory=list)
    spol_ic_date: Optional[datetime] = fd("Send SPOL to ins comp date", default=None)
    resolution: Optional[ClaimResolution] = fd("Claim resolution", default=None)
    resolution_amount: Optional[Decimal] = fd("Resolution Amount $", default=None)
    workflow: Optional[Workflow] = fd("State Workflow", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class OpenClaimRequirement:
    """
    Requeriment to open a claim
    """
    completed: bool = fd("Completed or not", default=False)
    description: str = fd("Requirement description", default='')
    module: str = fd("Module name to set requirement", default='')
