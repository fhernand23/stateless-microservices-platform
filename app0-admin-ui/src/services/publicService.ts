import axios from 'axios'
import { handleAPIError } from '/@src/services/handleAPIError'

const BASE_URL = import.meta.env.VITE_APP_API_URL
console.log(BASE_URL)

const apiClient = axios.create({
  baseURL: BASE_URL as string,
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

export const publicService = {
  async getEnabledPlans() {
    const ret = await apiClient.get('/plan-list-enabled').catch(handleAPIError)
    return ret.data
  },
  async saveNewRegistration(object: any) {
    const ret = await apiClient.post('/registration-pub-save', object).catch(handleAPIError)
    return ret.data
  },
  async addLogo(formData: FormData) {
    const ret = await apiClient.post(`/logo-upload`, formData).catch(handleAPIError)
    return ret.data
  },
  async getLogoBlob(filename: string) {
    const ret = await apiClient
      .get(`/logo-get?doc_id=${filename}`, { responseType: 'arraybuffer' })
      .catch(handleAPIError)
    return new Blob([ret.data], { type: 'application/octet-binary' })
  },
  getLogoURL(filename: string) {
    return `${BASE_URL}/logo-get?doc_id=${filename}`
  },
  async validateEmail(email: string) {
    const ret = await apiClient.get(`/user-validate-mail-unique?email=${email}`).catch(handleAPIError)
    return ret.data
  },
}
