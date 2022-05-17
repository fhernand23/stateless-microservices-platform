<script setup lang="ts">
import { useSession } from '/@src/stores/session'

const session = useSession()
</script>

<template>
  <div v-if="session.isAdmin" class="mobile-subsidebar is-activity">
    <div class="inner">
      <div class="sidebar-title">
        <h3>Settings</h3>
      </div>

      <ul class="submenu">
        <li class="divider with-label">
          <span class="divider-label">Platform </span>
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
