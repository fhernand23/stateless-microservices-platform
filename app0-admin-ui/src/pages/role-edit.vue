<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform Role',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <RoleForm />
    </div>
  </SidebarLayout>
</template>
