<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoading = ref(false)

router.beforeEach(() => {
  isLoading.value = true
})
router.afterEach(() => {
  setTimeout(() => {
    isLoading.value = false
  }, 200)
})
</script>

<template>
  <img src="../assets/logos/logo_transparent.svg" alt="Platform Logo" />
</template>

<style lang="scss" scoped>
img {
  height: 100px;
  width: 100px;
}
</style>
