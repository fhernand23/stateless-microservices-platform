<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform Users',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <UserList />
    </div>
  </SidebarLayout>
</template>
