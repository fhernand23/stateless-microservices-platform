<script setup lang="ts">
import { useHead } from '@vueuse/head'

useHead({
  title: 'Platform available plans',
})
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <PlanGrid />
    </div>
  </SidebarLayout>
</template>
