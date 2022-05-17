<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useHead } from '@vueuse/head'
import { useNotyf } from '/@src/composable/useNotyf'
import { useAuth } from '/@src/auth1'

import { useDarkmode } from '/@src/stores/darkmode'

const router = useRouter()
const notyf = useNotyf()
const darkmode = useDarkmode()
const isLoading = ref(false)
const route = useRoute()
const token = route.params.token as string
const newPassword = ref('')
const repeatPassword = ref('')

const vErrors = ref({
  min_length: false,
  mismatch: false,
})
const validateForm = () => {
  vErrors.value.min_length =
    !newPassword.value || !repeatPassword.value || newPassword.value.length < 6 || repeatPassword.value.length < 6
  vErrors.value.mismatch = newPassword.value !== repeatPassword.value

  return !vErrors.value.min_length && !vErrors.value.mismatch
}
const doReset = async () => {
  if (!isLoading.value) {
    isLoading.value = true
    try {
      if (validateForm()) {
        const ret = await useAuth.resetPassword({ auth_token: token, password: newPassword.value })
        if (ret.status == 200) {
          notyf.success('Reset successfull')
          router.push({ name: 'login' })
        } else {
          notyf.error('Reset successfull')
        }
      }
    } catch (error: any) {
      notyf.error(error.message)
    }
    isLoading.value = false
  }
}

useHead({
  title: 'Platform password reset',
})
</script>

<template>
  <AuthLayout>
    <div class="auth-wrapper-inner is-single">
      <!--Fake navigation-->
      <div class="auth-nav">
        <div class="left"></div>
        <div class="center">
          <RouterLink :to="{ name: 'index' }" class="header-item">
            <AppLogo width="38px" height="38px" />
          </RouterLink>
        </div>
        <div class="right">
          <label class="dark-mode ml-auto">
            <input type="checkbox" :checked="!darkmode.isDark" @change="darkmode.onChange" />
            <span></span>
          </label>
        </div>
      </div>

      <!--Single Centered Form-->
      <div class="single-form-wrap">
        <div class="inner-wrap">
          <!--Form Title-->

          <div class="auth-head">
            <h2>Reset your password</h2>
          </div>

          <!--Form-->
          <div class="form-card">
            <form @submit.prevent>
              <div class="login-form">
                <!-- Input -->
                <!-- <VField>
                  <VControl icon="feather:mail">
                    <input class="input" type="text" placeholder="Email Address" autocomplete="email" />
                  </VControl>
                </VField> -->
                <!-- Input -->
                <VField>
                  <VControl icon="feather:lock">
                    <input
                      v-model="newPassword"
                      class="input"
                      type="password"
                      placeholder="New Password"
                      autocomplete="new-password"
                    />
                  </VControl>
                </VField>
                <!-- Input -->
                <VField>
                  <VControl icon="feather:lock">
                    <input v-model="repeatPassword" class="input" type="password" placeholder="Repeat new Password" />
                  </VControl>
                </VField>

                <!-- Submit -->
                <VField>
                  <VControl class="login">
                    <VButton color="primary" bold fullwidth raised @click="doReset"> Reset Password </VButton>
                  </VControl>
                </VField>
                <VMessage v-if="vErrors.min_length" color="danger"
                  >New Password and Repeat new Password fields are required and should have a minimal length of 6
                  characters</VMessage
                >
                <VMessage v-if="vErrors.mismatch" color="danger"
                  >New Password and Repeat new Password fields should contains same value</VMessage
                >
              </div>
            </form>
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
