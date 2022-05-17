/**
 * Theses types are used by the Wizard form
 *
 * @see /src/pages/registration-wizard.vue
 */
export type RegistrationData = {
  id?: string
  status: string
  creation_date: string
  plan_id: string
  plan_name: string
  plan_description: string
  firstname: string
  surname: string
  email: string
  phone: string
  address: string
}

export type RegistrationValid = {
  firstname: boolean
  surname: boolean
  email: boolean
  phone: boolean
  address: boolean
  server_user_error_msg: string
}
