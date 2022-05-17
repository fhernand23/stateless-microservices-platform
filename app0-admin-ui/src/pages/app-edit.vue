<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform App',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <AppForm />
    </div>
  </SidebarLayout>
</template>
