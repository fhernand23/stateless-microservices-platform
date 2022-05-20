<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform Registrations',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <RegistrationList />
    </div>
  </SidebarLayout>
</template>
