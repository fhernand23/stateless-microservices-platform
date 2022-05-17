<script setup lang="ts">
import { useSession } from '/@src/stores/session'
import { useRouter } from 'vue-router'

const session = useSession()
const router = useRouter()

const goLogout = () => {
  router.push({ name: 'logout' })
}
</script>

<template>
  <VDropdown right spaced class="user-dropdown profile-dropdown">
    <template #button="{ toggle }">
      <a
        tabindex="0"
        class="is-trigger dropdown-trigger"
        aria-haspopup="true"
        @keydown.space.prevent="toggle"
        @click="toggle"
      >
        <Logo :image="session.userData.image" :name1="session.userData.fullname" size="small" />
      </a>
    </template>

    <template #content>
      <div class="dropdown-head">
        <Logo :image="session.userData.image" :name1="session.userData.fullname" size="large" />

        <div class="meta">
          <span>{{ session.userData.fullname }}</span>
          <span>{{ session.userData.user }}</span>
        </div>
      </div>

      <RouterLink :to="{ name: 'profile' }" role="menuitem" class="dropdown-item is-media">
        <div class="icon">
          <i aria-hidden="true" class="lnil lnil-user-alt"></i>
        </div>
        <div class="meta">
          <span>Profile</span>
          <span>View your profile</span>
        </div>
      </RouterLink>

      <hr class="dropdown-divider" />

      <div class="dropdown-item is-button">
        <VButton
          class="logout-button"
          icon="feather:log-out"
          color="primary"
          role="menuitem"
          raised
          fullwidth
          @click="goLogout()"
        >
          Logout
        </VButton>
      </div>
    </template>
  </VDropdown>
</template>
