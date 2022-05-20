<script setup lang="ts">
const emit = defineEmits(['close'])
</script>

<template>
  <div class="sidebar-panel is-generic">
    <div class="subpanel-header">
      <h3 class="no-mb">Settings</h3>
      <div class="panel-close" tabindex="0" @keydown.space.prevent="emit('close')" @click="emit('close')">
        <i aria-hidden="true" class="iconify" data-icon="feather:x"></i>
      </div>
    </div>
    <div class="inner" data-simplebar>
      <ul>
        <li class="divider with-label">
          <span class="divider-label">Platform</span>
        </li>
        <li>
          <RouterLink :to="{ name: 'registrations' }">Registrations</RouterLink>
        </li>
        <li class="divider"></li>
        <li class="divider with-label">
          <span class="divider-label">System options</span>
        </li>
        <li>
          <RouterLink :to="{ name: 'apps' }">Apps</RouterLink>
        </li>
        <li>
          <RouterLink :to="{ name: 'roles' }">Roles</RouterLink>
        </li>
        <li>
          <RouterLink :to="{ name: 'tmails' }">Mails</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss">
@import '/@src/scss/layout/sidebar-panel';
</style>
