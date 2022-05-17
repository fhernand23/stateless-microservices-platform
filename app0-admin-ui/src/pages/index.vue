<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSession } from '/@src/stores/session'
import { useHead } from '@vueuse/head'
import sleep from '/@src/utils/sleep'
import { useDarkmode } from '/@src/stores/darkmode'

useHead({
  title: 'Platform Home',
})

const router = useRouter()
const session = useSession()
const darkmode = useDarkmode()

onMounted(async () => {
  console.log('Current user: ' + session.userData?.user)
  console.log('isAuthenticated: ' + session.isAuthenticated)
  if (session.isAuthenticated) {
    console.log('User authenticated -> redirect to home')
    await sleep(400)
    router.push({ name: 'home' })
  } else {
    console.log('User not authenticated -> redirect to login')
    await sleep(400)
    router.push({ name: 'login' })
  }
})
</script>

<template>
  <MinimalLayout theme="light">
    <div class="landing-page-wrapper">
      <!-- Hero and Navbar -->
      <div id="vuer-landing" class="hero is-fullheight rounded-hero is-active">
        <div class="absolute-header">
          <div class="header-inner">
            <img class="cut-circle light-image-l" src="../assets/shapes/cut-circle.svg" alt="" />
            <img class="cut-circle dark-image-l" src="../assets/shapes/cut-circle-dark.svg" alt="" />
          </div>
        </div>

        <div class="hero-body has-text-centered">
          <div class="container">
            <div class="switch-wrapper">
              <div class="night-toggle night-toggle--daynight">
                <input
                  id="night-toggle--daynight"
                  type="checkbox"
                  class="night-toggle--checkbox"
                  :checked="!darkmode.isDark"
                  aria-label="Toggle dark mode"
                  @change="darkmode.onChange"
                />
                <label class="night-toggle--btn" for="night-toggle--daynight">
                  <span class="night-toggle--feature"></span>
                </label>
              </div>
            </div>
            <h1 class="title is-1 is-bold is-light is-bold"><span>App0</span> Platform</h1>
            <h3 class="subtitle is-4 is-light">An approach to a simple platform</h3>

            <img
              class="light-image-l hero-mockup"
              src="../assets/landing-01.png?width=740&height=490&format=webp"
              alt=""
            />
            <img
              class="dark-image-l hero-mockup"
              src="../assets/landing-01.png?width=740&height=490&format=webp"
              alt=""
            />
          </div>
        </div>

        <canvas id="demo-canvas"></canvas>
      </div>
    </div>
  </MinimalLayout>
</template>

<style lang="scss">
@import '/@src/scss/abstracts/all';
@import '/@src/scss/_demo/landing';
</style>
