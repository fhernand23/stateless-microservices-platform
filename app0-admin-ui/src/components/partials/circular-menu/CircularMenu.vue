<script setup lang="ts">
import { useWindowScroll } from '@vueuse/core'
import { ref, watchEffect } from 'vue'
import { useDarkmode } from '/@src/stores/darkmode'

const darkmode = useDarkmode()
const { y } = useWindowScroll()
const isOpen = ref(false)
const isScrolling = ref(false)

watchEffect(() => {
  if (y.value <= 30) {
    isOpen.value = false
  }

  isScrolling.value = y.value > 30
})
</script>

<template>
  <div id="circular-menu" :class="[isScrolling && 'is-active', isOpen && 'active']" class="circular-menu">
    <a class="floating-btn" tabindex="0" @keydown.space.prevent="isOpen = !isOpen" @click="isOpen = !isOpen">
      <i aria-hidden="true" class="fas fa-bars"></i>
      <i aria-hidden="true" class="fas fa-times"></i>
    </a>

    <div class="items-wrapper">
      <div class="menu-item is-flex">
        <label class="dark-mode">
          <input type="checkbox" :checked="!darkmode.isDark" @change="darkmode.onChange" />
          <span></span>
        </label>
      </div>
      <RouterLink :to="{ name: 'profile-notifications' }" class="menu-item is-flex">
        <i aria-hidden="true" class="iconify" data-icon="feather:bell"></i>
      </RouterLink>
      <a class="menu-item is-flex" href="/admin/home">
        <i aria-hidden="true" class="iconify" data-icon="feather:grid"></i>
      </a>
    </div>
  </div>
</template>

<style lang="scss">
.circular-menu {
  position: fixed;
  top: 0.6em;
  right: 1em;
  z-index: 70;
  transform: translateY(-80px);
  pointer-events: none;
  transition: transform 0.3s;

  &.is-active {
    pointer-events: all;
    transform: translateY(0);
  }

  &.active {
    &::after {
      transform: scale3d(5.5, 5.5, 1);
      transition-timing-function: cubic-bezier(0.68, 1.55, 0.265, 1);
    }

    .floating-btn {
      box-shadow: 0 4px 8px 0 hsl(0deg 0% 0% / 30%);

      i {
        &:first-child {
          display: none;
        }

        &:nth-child(2) {
          display: block;
        }
      }
    }

    .menu-item {
      transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);

      &:nth-child(1) {
        transform: translate3d(-7em, -0.5em, 0);
      }

      &:nth-child(2) {
        transform: translate3d(-6.25em, 3.25em, 0);
      }

      &:nth-child(3) {
        transform: translate3d(-3.45em, 6.25em, 0);
      }

      &:nth-child(4) {
        transform: translate3d(0.5em, 7em, 0);
      }
    }
  }

  &::after {
    display: block;
    content: ' ';
    width: 3.5em;
    height: 3.5em;
    border-radius: var(--radius-rounded);
    position: absolute;
    top: 0;
    right: 0;
    z-index: -2;
    background-color: var(--primary-dark-5);
    box-shadow: var(--primary-box-shadow);
    transition: all 0.3s ease;
  }

  .floating-btn {
    width: 3.5em;
    height: 3.5em;
    border-radius: var(--radius-rounded);
    background-color: var(--primary-light-3);
    box-shadow: var(--primary-box-shadow);
    color: var(--smoke-white);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;

    i {
      font-size: 0.9rem;
      transition: transform 0.2s;

      &:first-child {
        display: block;
      }

      &:nth-child(2) {
        display: none;
      }
    }
  }

  .items-wrapper {
    padding: 0;
    margin: 0;
  }

  .menu-item {
    position: absolute;
    top: 0.2em;
    right: 0.2em;
    z-index: -1;
    display: block;
    text-decoration: none;
    color: hsl(0deg 0% 100%);
    font-size: 1em;
    width: 3em;
    height: 3em;
    border-radius: var(--radius-rounded);
    text-align: center;
    line-height: 3;
    background-color: hsl(0deg 0% 0% / 20%);
    transition: transform 0.3s ease, background-color 0.2s ease;

    &:hover,
    &:focus {
      background-color: hsl(0deg 0% 0% / 30%);
    }

    &.is-flex {
      display: flex;
      align-items: center;
      justify-content: center;

      .dark-mode {
        transform: scale(0.5);
      }

      > img {
        display: block;
        height: 24px;
        width: 24px;
        min-width: 24px;
        border-radius: var(--radius-rounded);
      }

      svg {
        height: 18px;
        width: 18px;
        color: var(--smoke-white);
        stroke-width: 1.6px;
      }
    }
  }
}

.is-dark {
  .circular-menu {
    &::after {
      background: var(--dark-sidebar-dark-2);
      box-shadow: 0 4px 8px 0 hsl(0deg 0% 0% / 30%) !important;
    }

    &.active {
      .floating-btn {
        box-shadow: 0 4px 8px 0 hsl(0deg 0% 0% / 30%) !important;
      }
    }

    .floating-btn {
      background: var(--dark-sidebar-light-2);
      box-shadow: 0 4px 8px 0 hsl(0deg 0% 0% / 30%) !important;
    }
  }
}
</style>
