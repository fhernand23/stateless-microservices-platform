<script setup lang="ts">
import { useAuth } from '/@src/auth1'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(async () => {
  await useAuth.logout()
  router.push('/')
})
</script>

<template>
  <AuthLayout>
    <p>Logout...</p>
  </AuthLayout>
</template>
