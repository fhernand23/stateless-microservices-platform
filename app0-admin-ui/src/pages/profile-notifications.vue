<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform Notifications',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <NotificationPage />
    </div>
  </SidebarLayout>
</template>
