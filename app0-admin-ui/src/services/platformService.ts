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

export const platformService = {
  async getCurrUserApps() {
    const ret = await apiClient.get('/auth-user-apps').catch(handleAPIError)
    return ret.data
  },
  async getCurrUserRoles() {
    const ret = await apiClient.get('/auth-user-roles').catch(handleAPIError)
    return ret.data
  },
  async getCurrUserNotifications() {
    const ret = await apiClient.get('/auth-user-notifications').catch(handleAPIError)
    return ret.data
  },
  async getApps(filters: any) {
    const ret = await apiClient.post('/app-list', filters ? filters : {}).catch(handleAPIError)
    return ret.data
  },
  async getApp(obj_id: any) {
    const ret = await apiClient.get(`/app-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveApp(object: any) {
    const ret = await apiClient.post('/app-save', object).catch(handleAPIError)
    return ret.data
  },
  async saveAppAction(object: any, action: string) {
    const ret = await apiClient.post(`/app-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async getUsers(filters: any, page: number, pageSize: number) {
    const ret = await apiClient
      .post(`/user-list?page=${page}&page_size=${pageSize}`, filters ? filters : {})
      .catch(handleAPIError)
    return ret.data
  },
  async getUser(obj_id: any) {
    const ret = await apiClient.get(`/user-get?user_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveUser(object: any) {
    const ret = await apiClient.post('/user-save', object).catch(handleAPIError)
    return ret.data
  },
  async saveUserAction(object: any, action: string) {
    const ret = await apiClient.post(`/user-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async getRoles(filters: any) {
    const ret = await apiClient.post('/role-list', filters ? filters : {}).catch(handleAPIError)
    return ret.data
  },
  async getRole(obj_id: any) {
    const ret = await apiClient.get(`/role-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveRole(object: any) {
    const ret = await apiClient.post('/role-save', object).catch(handleAPIError)
    return ret.data
  },
  async saveRoleAction(object: any, action: string) {
    const ret = await apiClient.post(`/role-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async getCompanies(filters: any, page: number, pageSize: number) {
    const ret = await apiClient
      .post(`/company-list?page=${page}&page_size=${pageSize}`, filters ? filters : {})
      .catch(handleAPIError)
    return ret.data
  },
  async getCompany(obj_id: any) {
    const ret = await apiClient.get(`/company-get?company_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveCompany(object: any) {
    const ret = await apiClient.post('/company-save', object).catch(handleAPIError)
    return ret.data
  },
  async saveCompanyAction(object: any, action: string) {
    const ret = await apiClient.post(`/company-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async getCompanyData(obj_id: any, category: string, filters: any) {
    const ret = await apiClient
      .post(`/company-data?company_id=${obj_id}&category=${category}`, filters)
      .catch(handleAPIError)
    return ret.data
  },
  async getNotifications(filters: any) {
    const ret = await apiClient.post('/notification-list', filters).catch(handleAPIError)
    return ret.data
  },
  async getNotification(obj_id: any) {
    const ret = await apiClient.get(`/notification-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveNotification(object: any) {
    const ret = await apiClient.post('/notification-save', object).catch(handleAPIError)
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
  async getTmails(filters: any) {
    const ret = await apiClient.post('/tmail-list', filters).catch(handleAPIError)
    return ret.data
  },
  async getTmail(obj_id: any) {
    const ret = await apiClient.get(`/tmail-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveTmail(object: any) {
    const ret = await apiClient.post('/tmail-save', object).catch(handleAPIError)
    return ret.data
  },
  async getPlans(filters: any) {
    const ret = await apiClient.post('/plan-list', filters).catch(handleAPIError)
    return ret.data
  },
  async getPlan(obj_id: any) {
    const ret = await apiClient.get(`/plan-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async savePlan(object: any) {
    const ret = await apiClient.post('/plan-save', object).catch(handleAPIError)
    return ret.data
  },
  async savePlanAction(object: any, action: string) {
    const ret = await apiClient.post(`/plan-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async getRegistrations(filters: any) {
    const ret = await apiClient.post('/registration-list', filters).catch(handleAPIError)
    return ret.data
  },
  async getRegistration(obj_id: any) {
    const ret = await apiClient.get(`/registration-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveRegistration(object: any) {
    const ret = await apiClient.post('/registration-save', object).catch(handleAPIError)
    return ret.data
  },
  async saveRegistrationAction(object: any, action: string) {
    const ret = await apiClient.post(`/registration-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async getSubscriptions(filters: any) {
    const ret = await apiClient.post('/subscription-list', filters).catch(handleAPIError)
    return ret.data
  },
  async getSubscription(obj_id: any) {
    const ret = await apiClient.get(`/subscription-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveSubscription(object: any) {
    const ret = await apiClient.post('/subscription-save', object).catch(handleAPIError)
    return ret.data
  },
  async addCompanyFile(company_id: string, tag: string, formData: FormData) {
    const ret = await apiClient
      .post(`/company-file-upload?company_id=${company_id}&tag=${tag}`, formData)
      .catch(handleAPIError)
    return ret.data
  },
  async getCompanyFileObjectURL(company_id: string, doc_id: string) {
    const ret = await apiClient
      .get(`/company-file-get?company_id=${company_id}&doc_id=${doc_id}`, { responseType: 'arraybuffer' })
      .catch(handleAPIError)
    return window.URL.createObjectURL(new Blob([ret.data], { type: 'application/octet-binary' }))
  },
  async getCompanyFileBlob(company_id: string, doc_id: string) {
    const ret = await apiClient
      .get(`/company-file-get?company_id=${company_id}&doc_id=${doc_id}`, { responseType: 'arraybuffer' })
      .catch(handleAPIError)
    return new Blob([ret.data], { type: 'application/octet-binary' })
  },
  async getCompanyConfig(obj_id: any) {
    const ret = await apiClient.get(`/company-config-get?company_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveCompanyConfig(object: any) {
    const ret = await apiClient.post('/company-config-save', object).catch(handleAPIError)
    return ret.data
  },
  async getEvents(filters: any) {
    const ret = await apiClient.post('/event-list', filters).catch(handleAPIError)
    return ret.data
  },
  async getEvent(obj_id: any) {
    const ret = await apiClient.get(`/event-get?obj_id=${obj_id}`).catch(handleAPIError)
    return ret.data
  },
  async saveEvent(object: any) {
    const ret = await apiClient.post('/event-save', object).catch(handleAPIError)
    return ret.data
  },
  async getUserRoles(filters: any) {
    const ret = await apiClient.post('/user-role-list', filters).catch(handleAPIError)
    return ret.data
  },
  async saveUserRole(object: any) {
    const ret = await apiClient.post('/user-role-save', object).catch(handleAPIError)
    return ret.data
  },
  async saveUserRoleAction(object: any, action: string) {
    const ret = await apiClient.post(`/user-role-save?action=${action}`, object).catch(handleAPIError)
    return ret.data
  },
  async validateEmail(email: string) {
    const ret = await apiClient.get(`/user-validate-mail-unique?email=${email}`).catch(handleAPIError)
    return ret.data
  },
}
