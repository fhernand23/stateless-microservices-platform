<script setup lang="ts">
import { useHead } from '@vueuse/head'

let title = 'Platform Home'
useHead({ title: title })
</script>

<template>
  <SidebarLayout>
    <div class="page-content-inner">
      <HomeDashboard />
    </div>
  </SidebarLayout>
</template>
