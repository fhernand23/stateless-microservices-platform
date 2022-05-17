import { definePlugin } from '/@src/app'
import { authGuard } from '/@src/auth1/authGuard'

export default definePlugin(({ router }) => {
  router.beforeEach(authGuard)
})
