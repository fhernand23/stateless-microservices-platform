<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform apps',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <AppList />
    </div>
  </SidebarLayout>
</template>
