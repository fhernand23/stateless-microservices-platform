<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform roles',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <RoleList />
    </div>
  </SidebarLayout>
</template>
