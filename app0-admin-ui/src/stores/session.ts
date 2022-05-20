import { defineStore } from 'pinia'
import decode from 'jwt-decode'
import { ROLE_ADMIN } from '../data/constants'
import { ref } from 'vue'
export type UserData = Record<string, any> | null

interface State {
  userData: UserData
}

export const useSession = defineStore('session', {
  state: (): State => ({
    userData: ref<Partial<UserData>>(),
  }),
  actions: {
    setUser(payload: string) {
      this.userData = payload ? decode(payload) : null
    },
  },
  getters: {
    currentUser: (state) => {
      return state.userData
    },
    isAuthenticated: (state) => {
      return state.userData !== null
    },
    isAdmin: (state) => {
      return state.userData?.roles.includes(ROLE_ADMIN)
    },
  },
})
