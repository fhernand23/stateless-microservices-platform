import { reactive, ref, computed } from 'vue'

import type { RegistrationData, RegistrationValid } from '/@src/models/registrationWizard'

export const currentStep = ref(1)
export const isLoading = ref(false)

export const stepTitle = computed(() => {
  switch (currentStep.value) {
    case 2:
      return 'User Details'
    case 3:
      return 'Preview'
    case 4:
      return 'Finish'
    case 1:
    default:
      return 'Subscription Plan'
  }
})

export function resetData() {
  registrationData.id = undefined
  registrationData.plan_id = ''
  registrationData.plan_name = ''
  registrationData.plan_description = ''
  registrationData.firstname = ''
  registrationData.surname = ''
  registrationData.email = ''
  registrationData.phone = ''
  registrationData.address = ''
  registrationData.status = 'Incomplete'
  registrationData.creation_date = ''
}

export const registrationData = reactive<RegistrationData>({
  id: undefined,
  plan_id: '',
  plan_name: '',
  plan_description: '',
  firstname: '',
  surname: '',
  email: '',
  phone: '',
  address: '',
  status: 'Incomplete',
  creation_date: '',
})

export const registrationValid = reactive<RegistrationValid>({
  firstname: false,
  surname: false,
  email: false,
  phone: false,
  address: false,
  server_user_error_msg: '',
})
