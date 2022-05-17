<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Mail Template',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <TmailForm />
    </div>
  </SidebarLayout>
</template>
