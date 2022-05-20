export interface IdDescription {
  value: string
  label: string
  internal_id?: string
  details?: Object
}

export interface PlatformFile {
  bucket: string
  filename: string
  size: number
  src_filename: string
  object_id: string
  creation_date?: string
}

export interface User {
  id?: string
  username: string
  firstname: string
  surname: string
  email: string
  phone_number: string
  employee_id: string
  company_representative?: boolean
  enabled?: boolean
}

export interface Company {
  id?: string
  name: string
  fantasy_name?: string
  ssn_ein?: string
  address: string
  phone_number: string
  email: string
  image?: string
  alt_emails?: string[]
  alt_phones?: string[]
}

export interface CompanyConfig {
  id?: string
  w9_document_mandatory?: boolean
  w9_document_date?: string
  w9_document_resource?: PlatformFile
  lor_document_mandatory?: boolean
  lor_document_date?: string
  lor_document_resource?: PlatformFile
  spol_document_mandatory?: boolean
  spol_document_date?: string
  spol_document_resource?: PlatformFile
  attorney_list_mandatory?: boolean
  attorney_list_date?: string
  attorney_list_resource?: PlatformFile
}

export interface AppRole {
  id?: string
  name: string
  description: string
  application?: string
  can_delete?: boolean
  enabled?: boolean
}

export interface AppDef {
  id?: string
  name: string
  description: string
  url: string
  default_role: string
  image?: string
  enabled?: boolean
}
