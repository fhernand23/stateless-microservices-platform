<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDropdown } from '/@src/composable/useDropdown'
import { currentStep, stepTitle } from '/@src/state/registrationWizardState'
import { useDarkmode } from '/@src/stores/darkmode'

const router = useRouter()
const darkmode = useDarkmode()
const dropdownElement1 = ref<HTMLElement>()
const dropdown1 = useDropdown(dropdownElement1)

const setStep = (target: number) => {
  if (currentStep.value >= target) {
    currentStep.value = target
    dropdown1.close()
  }
}

const cancelRegistration = () => {
  router.push({ name: 'home' })
}
</script>

<template>
  <nav class="wizard-navigation">
    <RouterLink :to="{ name: 'index' }" class="wizard-brand">
      <AppLogo width="38px" height="38px" />
    </RouterLink>

    <div class="navbar-item is-wizard-title" @click="dropdown1.toggle">
      <span class="title-wrap">
        Step {{ currentStep }}: <span>{{ stepTitle }}</span>
      </span>
    </div>

    <div ref="dropdownElement1" class="dropdown wizard-dropdown dropdown-trigger">
      <div class="is-trigger" @click="dropdown1.toggle">
        <i aria-hidden="true" class="iconify" data-icon="feather:chevron-down"></i>
      </div>
      <div id="wizard-navigation-dropdown" class="dropdown-menu" role="menu">
        <div class="dropdown-content">
          <a :class="[currentStep < 1 && 'is-disabled']" class="dropdown-item kill-drop" @click="setStep(1)">
            Step 1: Subscription Plan
          </a>
          <a :class="[currentStep < 2 && 'is-disabled']" class="dropdown-item kill-drop" @click="setStep(2)">
            Step 2: User Details
          </a>
          <a :class="[currentStep < 3 && 'is-disabled']" class="dropdown-item kill-drop" @click="setStep(3)">
            Step 3: Preview
          </a>
          <a :class="[currentStep < 4 && 'is-disabled']" class="dropdown-item kill-drop" @click="setStep(4)">
            Step 4: Finish
          </a>
        </div>
      </div>
    </div>

    <div class="navbar-item is-dark-mode">
      <div class="navbar-icon">
        <label class="dark-mode">
          <input
            type="checkbox"
            :checked="!darkmode.isDark"
            aria-label="Toggle dark mode"
            @change="darkmode.onChange"
          />
          <span></span>
        </label>
      </div>
    </div>

    <div class="dropdown is-right dropdown-trigger user-dropdown">
      <div class="is-trigger" aria-haspopup="true" @click="cancelRegistration()">
        <div class="profile-avatar">
          <i aria-hidden="true" class="iconify" data-icon="feather:grid"></i>
        </div>
      </div>
    </div>
  </nav>
</template>

<style lang="scss" scoped>
@import '/@src/scss/abstracts/all';

.wizard-navigation {
  position: fixed;
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 60px;
  background: var(--white);
  padding: 0 20px;
  transition: all 0.3s;
  z-index: 99;

  .wizard-brand {
    img {
      display: block;
      height: 34px;
      margin: 0 auto;
    }
  }

  .navbar-item {
    &.is-wizard-title {
      margin-left: 15px;
      border-left: 1px solid var(--muted-grey-light-15);
      padding-bottom: 6px;
      padding-top: 6px;
      font-family: var(--font);

      .title-wrap {
        position: relative;
        display: block;
        font-family: var(--font-alt);
        font-size: 1.2rem;
        font-weight: 600;

        span {
          font-weight: 400;
        }
      }
    }
  }

  .wizard-dropdown {
    cursor: pointer;

    .is-trigger {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 30px;
      height: 30px;

      svg {
        height: 18px;
        width: 18px;
        color: var(--light-text);
      }
    }

    .dropdown-menu {
      border: 1px solid var(--fade-grey-dark-3);
      box-shadow: var(--light-box-shadow);
      border-radius: 8px;
      padding-top: 0;
      overflow: hidden;

      .dropdown-content {
        .dropdown-item {
          font-family: var(--font);
        }
      }
    }
  }

  .is-dark-mode {
    margin-left: auto;
    background: transparent !important;

    .navbar-icon {
      height: 38px;
      width: 38px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--radius-rounded);
      border: 1px solid var(--fade-grey-dark-3);
      box-shadow: var(--light-box-shadow);
      background: var(--white);
      transition: all 0.3s;

      .dark-mode {
        transform: scale(0.6);
      }
    }
  }

  .user-dropdown {
    .is-trigger {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      cursor: pointer;

      .profile-avatar {
        position: relative;

        .avatar {
          display: block;
          width: 38px;
          height: 38px;
          border-radius: var(--radius-rounded);
        }

        .badge {
          position: absolute;
          right: -8px;
          bottom: 0;
          width: 20px;
          height: 20px;
          border: 2px solid var(--white);
          border-radius: var(--radius-rounded);
        }
      }

      svg {
        margin-left: 3px;
        width: 18px;
        height: 18px;
        color: var(--light-text);
        transition: all 0.3s;
      }
    }

    .dropdown-menu {
      top: 52px;
      border: 1px solid var(--fade-grey-dark-3);
      box-shadow: var(--light-box-shadow);
      border-radius: 8px;
      padding-top: 0;
      width: 180px;
      overflow: hidden;

      .dropdown-item {
        display: flex;
        align-items: center;
        font-family: var(--font);
        font-size: 0.9rem;
        padding: 8px 12px;
        color: var(--light-text);

        p {
          font-family: var(--font-alt);
          font-weight: 600;
          font-size: 0.95rem;
          color: var(--dark-text);
        }

        svg {
          margin-right: 8px;
          height: 16px;
          width: 16px;
          color: var(--light-text);
        }
      }
    }
  }
}
</style>
