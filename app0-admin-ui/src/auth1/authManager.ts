import { AxiosInstance } from 'axios'
import decode from 'jwt-decode'

// API endpoints
// eslint-disable-next-line no-unused-vars
const REFRESH = '/refresh'
const AUTHORIZE = '/refresh'
const LOGIN = '/login'
const LOGOUT = '/logout'
const LOGIN_UI = '/admin/login'
const FORGOT = '/recovery'
const RESET = '/reset'
const DEFAULT_HOME = '/admin/home'

type AuthNew = {
  auth_token: string
  password: string
}

export default class AuthManager {
  private token: any
  private useStore: any
  private userSession = null
  private api: any
  private loading: boolean

  constructor(api: any, store: any) {
    this.token = null
    this.useStore = store
    this.userSession = null
    this.api = api
    this.loading = true
  }

  setToken() {
    if (!this.userSession) this.userSession = this.useStore()
    if (this.userSession) {
      this.userSession.setUser(this.token)
    }
    console.log(this.token !== undefined ? 'Set Token' : 'Unset Token')
  }

  authHeader() {
    return `Bearer ${this.token}`
  }
  get isAuthenticated() {
    return this.token !== null
  }

  get roles() {
    if (this.token) return decode(this.token).roles
    return []
  }

  get isLoading() {
    return this.loading
  }

  async selfLogin() {
    try {
      const ret = await this.api.get(AUTHORIZE)
      console.log('selfLogin')
      if (ret.status == 200) {
        this.token = ret.data.access_token
        this.setToken()
      }
      return true
    } catch (error) {
      console.log('error in selfLogin')
      return false
    }
  }

  async login(user: any, pass: any) {
    try {
      const ret = await this.api.get(LOGIN, {
        headers: {
          Accept: 'application/json, application/json',
          'Cache-Control': 'no-cache',
        },
        auth: {
          username: user,
          password: pass,
        },
      })
      console.log('login return')
      console.log(ret.data)
      this.token = ret.data.access_token
      this.setToken()
      return {
        loggedIn: true,
        status: ret.status,
      }
    } catch (err) {
      return {
        loggedIn: false,
        status: err.response ? err.response.status : 0,
      }
    }
  }

  async logout() {
    await this.api.get(LOGOUT, { withCredentials: true })
    this.token = null
    this.setToken()
  }

  async forgotPassword(user: Object) {
    return await this.api.post(FORGOT, user)
  }
  async resetPassword(AuthNew: AuthNew) {
    return await this.api.post(RESET, AuthNew)
  }

  loginWithRedirect(options: any) {
    let redirect_uri = LOGIN_UI
    if (
      options.appState.targetUrl &&
      options.appState.targetUrl !== LOGOUT &&
      options.appState.targetUrl !== DEFAULT_HOME
    ) {
      redirect_uri += `?redirect=${options.appState.targetUrl}`
    }
    window.location.assign(redirect_uri)
  }

  async bindToken(apiClient: AxiosInstance) {
    // if (this.loading) await this.selfLogin();
    if (this.token) {
      apiClient.defaults.headers.common.Authorization = this.authHeader()
    }

    apiClient.interceptors.request.use(
      async (config) => {
        if (!this.token) {
          try {
            const ret = await this.api.get(REFRESH)
            if (ret.status == 200) {
              this.token = ret.data.access_token
              this.setToken()
              console.log('req interceptor')
              config.headers.common.Authorization = this.authHeader()
              apiClient.defaults.headers.common.Authorization = this.authHeader()
            }
            return config
          } catch {
            window.location.assign(LOGOUT)
            return Promise.reject()
          }
        }
        return config
      },
      (error) => {
        Promise.reject(error)
      }
    )

    apiClient.interceptors.response.use(
      (response) => {
        return response
      },
      async (error) => {
        const originalRequest = error.config
        const noAuth = error.config.headers.Authorization === 'undefined'
        if (noAuth && this.token) {
          originalRequest.headers.Authorization = this.authHeader()
          apiClient.defaults.headers.common.Authorization = this.authHeader()
          return apiClient(originalRequest)
        } else if (error.response.status === 400 && !originalRequest._retry) {
          originalRequest._retry = true
          try {
            const res = await this.api.get(REFRESH)
            if (res.status == 200) {
              this.token = res.data.access_token
              apiClient.defaults.headers.common.Authorization = this.authHeader()
              originalRequest.headers.Authorization = this.authHeader()
              return apiClient(originalRequest)
            }
            return Promise.reject(error)
          } catch {
            this.setToken()
            return await Promise.reject(error)
          }
        } else {
          // any other error continue code to handle properly
          return Promise.reject(error)
        }
      }
    )
  }
}
