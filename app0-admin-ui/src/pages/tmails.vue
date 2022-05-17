<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform email templates',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <TmailList />
    </div>
  </SidebarLayout>
</template>
