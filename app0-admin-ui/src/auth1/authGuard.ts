import { useAuth } from '/@src/auth1/authService'

export const authGuard = async (to: any, from: any, next: () => any) => {
  if (!to.meta.requiresAuth) {
    return next()
  }
  if (useAuth.isAuthenticated || (await useAuth.selfLogin())) {
    return next()
  } else {
    useAuth.loginWithRedirect({ appState: { targetUrl: to.href } })
    return next()
  }
}
