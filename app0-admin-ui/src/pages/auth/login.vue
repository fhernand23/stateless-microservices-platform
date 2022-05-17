<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useHead } from '@vueuse/head'

import { useDarkmode } from '/@src/stores/darkmode'
import { useNotyf } from '/@src/composable/useNotyf'
import { useAuth } from '/@src/auth1'
import { APP_ADMIN_PREFIX, APP_APP1_PREFIX } from '/@src/data/constants'

const isLoading = ref(false)
const darkmode = useDarkmode()
const router = useRouter()
const route = useRoute()
const notif = useNotyf()
const redirect: string | undefined = route.query.redirect as string

const username = ref()
const password = ref()
type StepId = 'login' | 'forgot-password' | 'recovery'
const step = ref<StepId>('login')
const vErrors = ref({ emailOk: '' })

const doLogin = async () => {
  if (!isLoading.value) {
    let res = await useAuth.login(username.value, password.value)
    let status: number = res.status
    if (res.loggedIn) {
      notif.success(`Welcome back, ${username.value}`)

      if (redirect && redirect.startsWith(APP_ADMIN_PREFIX)) {
        router.push(redirect.replace('/admin', ''))
      } else if (redirect && redirect.startsWith(APP_APP1_PREFIX)) {
        window.open(redirect, '_self')
      } else {
        router.push('home')
      }
    } else {
      if (status === 401) {
        notif.error('Incorrect username or password, please try again')
      } else {
        notif.error('Unexpected error')
      }
    }
    isLoading.value = false
  }
}

const doForgot = async () => {
  const valid = username.value != ''
  if (valid) {
    let ret = await useAuth.forgotPassword(username.value)
    if (ret?.status != 200) {
      notif.error('Unexpected error reseting password')
    }
    step.value = 'recovery'
  } else {
    step.value = 'forgot-password'
  }
}

// const validateEmail = (val: string) => {
//   if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(val)) {
//     vErrors.value.emailOk = ''
//     return true
//   } else {
//     vErrors.value.emailOk = 'Please enter a valid email address'
//     return false
//   }
// }

useHead({
  title: 'App0 Platform',
})
</script>

<template>
  <AuthLayout>
    <div class="auth-wrapper-inner columns is-gapless">
      <!-- Image section (hidden on mobile) -->
      <div class="column login-column is-8 h-hidden-mobile h-hidden-tablet-p hero-banner">
        <div class="hero login-hero is-fullheight is-app-grey">
          <div class="hero-body">
            <div class="columns">
              <div class="column is-10 is-offset-1">
                <img
                  class="light-image has-light-shadow has-light-border"
                  src="../../assets/login_light.png?format=webp"
                  alt=""
                />
                <img class="dark-image has-light-shadow" src="../../assets/login_dark.png?format=webp" alt="" />
              </div>
            </div>
          </div>
          <div class="hero-footer">
            <p class="has-text-centered"></p>
          </div>
        </div>
      </div>

      <!-- Form section -->
      <div class="column is-4">
        <div class="hero is-fullheight is-white">
          <div class="hero-heading">
            <label class="dark-mode ml-auto">
              <input type="checkbox" :checked="!darkmode.isDark" @change="darkmode.onChange" />
              <span></span>
            </label>
            <div class="auth-logo has-text-centered">
              <RouterLink :to="{ name: 'index' }" class="header-item">
                <AppLogo width="100px" height="100px" />
                <h2>Platform</h2>
              </RouterLink>
            </div>
          </div>
          <div class="hero-body">
            <div class="container">
              <div class="columns">
                <div class="column is-12">
                  <div class="auth-content">
                    <div class="form-text" :class="[step !== 'login' && 'is-hidden']">
                      <h2>Sign In</h2>
                      <p>Welcome back to your account.</p>
                    </div>
                    <div class="form-text" :class="[step !== 'forgot-password' && 'is-hidden']">
                      <h2>Password recovery</h2>
                      <p>Reset your account password.</p>
                    </div>
                    <div class="form-text" :class="[step !== 'recovery' && 'is-hidden']">
                      <h2>Email sended!</h2>
                      <p>Please check your email inbox.</p>
                      <VMessage color="primary"
                        ><div>
                          <span>
                            We send you an email detailing the steps to complete the password recovery procedure.
                          </span>
                        </div></VMessage
                      >
                    </div>
                  </div>
                  <div class="auth-form-wrapper">
                    <!-- Login Form -->
                    <form :class="[step !== 'login' && 'is-hidden']" @submit.prevent="doLogin">
                      <div class="login-form">
                        <VField>
                          <VControl icon="feather:user">
                            <input
                              v-model="username"
                              class="input"
                              type="text"
                              placeholder="Username or email"
                              autocomplete="username"
                            />
                          </VControl>
                        </VField>
                        <VField>
                          <VControl icon="feather:lock">
                            <input
                              v-model="password"
                              class="input"
                              type="password"
                              placeholder="Password"
                              autocomplete="current-password"
                            />
                          </VControl>
                        </VField>
                        <div class="forgot-link has-text-right">
                          <a @click="step = 'forgot-password'">Forgot your password?</a>
                        </div>
                        <!-- Switch
                        <div class="control is-flex">
                          <VControl class="setting-item">
                            <label for="remember-me" class="form-switch is-primary">
                              <input id="remember-me" type="checkbox" class="is-switch" />
                              <i aria-hidden="true"></i>
                            </label>
                            <div class="setting-meta">
                              <label for="remember-me">
                                <span>Remember Me</span>
                              </label>
                            </div>
                          </VControl>
                        </div> -->

                        <!-- Submit -->
                        <div class="button-wrap has-help">
                          <VControl class="login">
                            <VButton :loading="isLoading" type="submit" color="primary" bold fullwidth raised>
                              Sign In
                            </VButton>
                          </VControl>
                          <div class="register-link">
                            <br />
                            Don't have an account yet?
                            <RouterLink
                              :to="{ name: 'registration-wizard' }"
                              :class="[step === 'recovery' && 'is-hidden']"
                              >Register now
                            </RouterLink>
                          </div>
                        </div>
                      </div>
                    </form>
                    <form :class="[step !== 'forgot-password' && 'is-hidden']" class="login-wrapper" @submit.prevent>
                      <VMessage color="primary">
                        <div>
                          <span
                            >An email will be sended detailing the steps to complete the password reset procedure.</span
                          >
                        </div>
                      </VMessage>
                      <p></p>
                      {{ vErrors.emailOk }}
                      <VField>
                        <VControl icon="feather:mail" :has-error="vErrors.emailOk !== ''">
                          <input
                            v-model="username"
                            class="input"
                            type="text"
                            placeholder="email"
                            autocomplete="username"
                          />
                          <small>Requires your primary email address.</small>
                        </VControl>
                      </VField>

                      <div>
                        <VButtons fullwidth>
                          <VButton color="primary" size="big" type="submit" bold fullwidth raised @click="doForgot">
                            Reset pasword
                          </VButton>
                        </VButtons>

                        <div class="has-text-centered">
                          Already have login and password?
                          <a @click="step = 'login'">Sign in</a>
                        </div>
                      </div>
                    </form>
                    <form :class="[step !== 'recovery' && 'is-hidden']" class="login-wrapper" @submit.prevent>
                      <div>
                        <VButtons>
                          <VButton color="primary" size="big" lower fullwidth @click="step = 'login'">Continue</VButton>
                        </VButtons>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AuthLayout>
</template>

<style lang="scss">
/*! _auth.scss */

/*
    1. Login / Signup v2
    3. Login / Signup v2 Dark mode
    4. Login / Signup v3
    5. Login / Signup v3 Dark mode
    6. Media Queries
*/

/* ==========================================================================
1. Login / Signup v2
========================================================================== */

.auth-wrapper-inner {
  overflow: hidden !important;
  height: 100%;
  padding: 0;
  margin: 0;

  &.is-gapless:not(:last-child) {
    margin-bottom: 0 !important;
  }

  &.is-single {
    background: var(--widget-grey);
    min-height: 100vh;
  }

  .hero-banner {
    background: var(--widget-grey);
  }

  .hero-heading {
    position: relative;
    max-width: 360px;
    width: 100%;
    margin: 0 auto;
    padding: 20px 0 0;

    .dark-mode {
      position: absolute;
      top: 24px;
      right: 24px;
      transform: scale(0.6);
      z-index: 2;
    }

    .auth-logo {
      display: flex;
      justify-content: center;

      svg {
        height: 42px;
        width: 42px;
      }

      .top-logo {
        height: 42px;
      }
    }
  }

  .hero {
    &.is-white {
      background: var(--white);
    }

    .hero-body {
      .login {
        padding: 10px 0;
      }

      .auth-content {
        max-width: 320px;
        width: 100%;
        margin: 0 auto;
        margin-top: -40px;
        margin-bottom: 40px;

        h2 {
          font-size: 2rem;
          font-family: var(--font);
          line-height: 1;
        }

        p {
          font-size: 1rem;
          margin-bottom: 8px;
          color: var(--muted-grey);
        }

        a {
          font-size: 0.9rem;
          font-family: var(--font-alt);
          font-weight: 500;
          color: var(--primary);
        }
      }

      .auth-form-wrapper {
        max-width: 320px;
        width: 100%;
        margin: 0 auto;
      }
    }
  }

  .forgot-link {
    margin-top: 10px;

    a {
      font-family: var(--font-alt);
      font-size: 0.9rem;
      color: var(--light-text) !important;
      transition: color 0.3s;

      &:hover {
        color: var(--primary) !important;
      }
    }
  }

  .register-link {
    margin-top: 10px;
    font-family: var(--font-alt);
    font-size: 0.9rem;

    a {
      font-family: var(--font-alt);
      font-size: 0.9rem;
      color: var(--light-text) !important;
      transition: color 0.3s;

      &:hover {
        color: var(--primary) !important;
      }
    }
  }

  .setting-item {
    display: flex;
    align-items: center;
    padding: 10px 0;

    .setting-meta {
      font-family: var(--font);
      color: var(--light-text);
      margin-left: 8px;
    }
  }

  .v-button {
    min-height: 44px;
  }
}

/* ==========================================================================
2. Login / Signup v2 Dark mode
========================================================================== */

.is-dark {
  .auth-wrapper-inner {
    .hero-banner {
      background: var(--dark-sidebar-light-4);
    }

    .hero {
      &.is-white {
        background: var(--dark-sidebar-dark-4);
      }

      .hero-body {
        .auth-content {
          h2 {
            color: var(--dark-dark-text);
          }

          a {
            color: var(--primary);
          }
        }
      }
    }

    .forgot-link {
      a:hover {
        color: var(--primary);
      }
    }

    .register-link {
      a:hover {
        color: var(--primary);
      }
    }
  }
}

/* ==========================================================================
3. Login / Signup v3
========================================================================== */

.auth-nav {
  position: absolute;
  top: 0;
  left: 0;
  height: 80px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;

  .left,
  .right {
    display: flex;
    align-items: center;
    width: 20%;
  }

  .right {
    justify-content: flex-end;

    .dark-mode {
      transform: scale(0.7);
    }
  }

  .center {
    flex-grow: 2;

    a {
      display: flex;
      justify-content: center;
      align-items: center;

      img {
        display: block;
        width: 100%;
        max-width: 50px;
      }
    }
  }
}

.auth-wrapper-inner {
  .single-form-wrap {
    min-height: 690px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: center;

    .inner-wrap {
      width: 100%;
      max-width: 400px;
      margin: 40px auto 0;

      .auth-head {
        max-width: 320px;
        width: 100%;
        margin: 0 auto;
        margin-bottom: 20px;
        text-align: center;

        h2 {
          font-size: 2rem;
          font-family: var(--font);
          line-height: 1;
        }

        p {
          font-size: 1rem;
          margin-bottom: 8px;
          color: var(--muted-grey);
        }

        a {
          font-size: 0.9rem;
          font-family: var(--font-alt);
          font-weight: 500;
          color: var(--primary);
        }
      }

      .form-card {
        background: var(--white);
        border: 1px solid var(--fade-grey-dark-3);
        border-radius: 10px;
        padding: 50px;
        margin-bottom: 16px;

        .v-button {
          margin-top: 10px;
        }
      }
    }
  }
}

/* ==========================================================================
4. Login / Signup v3 Dark mode
========================================================================== */

.is-dark {
  .auth-wrapper-inner {
    &.is-single {
      background: var(--dark-sidebar-light-4);

      .single-form-wrap {
        .inner-wrap {
          .auth-head {
            h2 {
              color: var(--dark-dark-text);
            }

            a {
              color: var(--primary);
            }
          }

          .form-card {
            background: var(--dark-sidebar-dark-4);
            border-color: var(--dark-sidebar-light-1);
          }
        }
      }
    }
  }
}

/* ==========================================================================
5. Media Queries
========================================================================== */

@media only screen and (max-width: 767px) {
  .avatar-carousel {
    &.resized-mobile {
      max-width: 300px;
    }

    .slick-custom {
      display: none !important;
    }

    .image-wrapper img {
      height: auto;
    }
  }

  .auth-wrapper-inner {
    .hero {
      .hero-body {
        .auth-content {
          text-align: center !important;
        }
      }
    }

    .single-form-wrap {
      .inner-wrap {
        .form-card {
          padding: 40px;
        }
      }
    }
  }
}

@media only screen and (min-width: 768px) and (max-width: 1024px) and (orientation: portrait) {
  .modern-login {
    .top-logo {
      svg {
        height: 60px;
        width: 60px;
      }
    }

    .dark-mode {
      top: -58px;
      right: 30%;
    }

    .columns {
      display: flex;
      height: 100vh;
    }
  }

  .auth-wrapper-inner {
    .hero {
      .hero-body {
        .auth-content {
          text-align: center !important;
        }
      }
    }
  }

  .signup-columns {
    max-width: 460px;
    margin: 0 auto;
  }
}
</style>
