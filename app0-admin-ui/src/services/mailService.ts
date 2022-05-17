import axios from 'axios'
import { useAuth } from '/@src/auth1'
import { handleAPIError } from '/@src/services/handleAPIError'

const BASE_URL = import.meta.env.VITE_APP_API_URL

const apiClient = axios.create({
  baseURL: BASE_URL as string,
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})
useAuth.bindToken(apiClient)

export const mailService = {
  async testEmail() {
    const ret = await apiClient.get(`/setup-adhoc?code=TEST_HTML_MAIL`).catch(handleAPIError)
    return ret.data
  },
  async testAttachFile() {
    const ret = await apiClient.get(`/setup-adhoc?code=TEST_ATT_FILE`).catch(handleAPIError)
    return ret.data
  },
  async testAttachS3() {
    const ret = await apiClient.get(`/setup-adhoc?code=TEST_ATT_S3`).catch(handleAPIError)
    return ret.data
  },
  async testTmail(object: any) {
    const ret = await apiClient.post('/mail-test', object).catch(handleAPIError)
    return ret.data
  },
}
