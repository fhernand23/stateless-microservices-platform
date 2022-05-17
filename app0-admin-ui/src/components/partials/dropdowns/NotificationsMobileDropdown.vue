<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { useDropdown } from '/@src/composable/useDropdown'
import { platformService } from '/@src/services/platformService'
import { utils } from '/@src/services/utils'

const dropdownElement = ref<HTMLElement>()
const dropdown = useDropdown(dropdownElement)
// TODO how to check if user has pending notifications
const hasPendingNotifications = ref(false)
const notifications = ref({})

onBeforeMount(async () => {
  let ret = await platformService.getCurrUserNotifications()
  notifications.value = ret.results
})
</script>

<template>
  <div ref="dropdownElement" class="navbar-item has-dropdown is-notification is-hidden-tablet is-hidden-desktop">
    <a class="navbar-link is-arrowless" tabindex="0" @keydown.space.prevent="dropdown.toggle" @click="dropdown.toggle">
      <i aria-hidden="true" class="iconify" data-icon="feather:bell"></i>
      <span v-if="hasPendingNotifications" class="new-indicator pulsate"></span>
    </a>
    <div class="navbar-dropdown is-boxed is-right">
      <div class="heading">
        <div class="heading-left">
          <h6 class="heading-title">Notifications</h6>
        </div>
        <div class="heading-right">
          <RouterLink class="notification-link" :to="{ name: 'profile-notifications' }"> See all </RouterLink>
        </div>
      </div>
      <div class="inner has-slimscroll">
        <ul class="notification-list">
          <li v-for="item in notifications" :key="item.id">
            <a class="notification-item">
              <div class="img-left">
                <VIconBox size="small" :color="utils.getNotificationColor(item.type)" rounded>
                  <i class="iconify" :data-icon="utils.getNotificationImage(item.type)"></i>
                </VIconBox>
              </div>
              <div class="user-content">
                <p class="user-info">
                  <span class="name">{{ item.user_name }}</span> {{ item.content }}
                </p>
                <p class="time">{{ utils.dateFmtStrH(item.creation_date) }}</p>
              </div>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
