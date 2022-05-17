<script setup lang="ts">
import { ref, watchPostEffect, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSession } from '/@src/stores/session'
import { ROLE_ADMIN } from '/@src/data/constants'
import type { SidebarTheme } from '/@src/components/navigation/desktop/Sidebar.vue'
import { useViewWrapper } from '/@src/stores/viewWrapper'

const props = withDefaults(
  defineProps<{
    theme?: SidebarTheme
    defaultSidebar?: string
    closeOnChange?: boolean
    openOnMounted?: boolean
    nowrap?: boolean
  }>(),
  {
    defaultSidebar: 'settings',
    theme: 'color-curved',
  }
)

const viewWrapper = useViewWrapper()
const route = useRoute()
const session = useSession()
const isMobileSidebarOpen = ref(false)
const isDesktopSidebarOpen = ref(props.openOnMounted)
const activeMobileSubsidebar = ref(props.defaultSidebar)

function switchSidebar(id: string) {
  if (id === activeMobileSubsidebar.value) {
    isDesktopSidebarOpen.value = !isDesktopSidebarOpen.value
  } else {
    isDesktopSidebarOpen.value = true
    activeMobileSubsidebar.value = id
  }
}

const isAdmin = computed(() => {
  if (session.userData?.roles) {
    return session.userData.roles.includes(ROLE_ADMIN)
  }
  return false
})

/**
 * watchPostEffect callback will be executed each time dependent reactive values has changed
 */
watchPostEffect(() => {
  viewWrapper.setPushed(isDesktopSidebarOpen.value ?? false)
})
watch(
  () => route.fullPath,
  () => {
    isMobileSidebarOpen.value = false

    if (props.closeOnChange && isDesktopSidebarOpen.value) {
      isDesktopSidebarOpen.value = false
    }
  }
)
</script>

<template>
  <div class="sidebar-layout">
    <div class="app-overlay"></div>

    <!-- Mobile navigation -->
    <MobileNavbar :is-open="isMobileSidebarOpen" @toggle="isMobileSidebarOpen = !isMobileSidebarOpen">
      <template #brand>
        <RouterLink :to="{ name: 'index' }" class="navbar-item is-brand">
          <AppLogo width="38px" height="38px" />
        </RouterLink>

        <div class="brand-end">
          <NotificationsMobileDropdown />
          <UserProfileDropdown />
        </div>
      </template>
    </MobileNavbar>

    <!-- Mobile sidebar links -->
    <MobileSidebar :is-open="isMobileSidebarOpen" @toggle="isMobileSidebarOpen = !isMobileSidebarOpen">
      <template #links>
        <li v-if="isAdmin">
          <RouterLink :to="{ name: 'users' }">
            <i aria-hidden="true" class="iconify" data-icon="icon-park-outline:peoples"></i>
          </RouterLink>
        </li>
        <li v-if="isAdmin">
          <RouterLink :to="{ name: 'plans' }">
            <i aria-hidden="true" class="iconify" data-icon="icon-park-outline:ad-product"></i>
          </RouterLink>
        </li>
      </template>

      <template #bottom-links>
        <li v-if="isAdmin">
          <a
            aria-label="Display Settings content"
            :class="[activeMobileSubsidebar === 'settings' && 'is-active']"
            tabindex="0"
            @keydown.space.prevent="activeMobileSubsidebar = 'settings'"
            @click="activeMobileSubsidebar = 'settings'"
          >
            <i aria-hidden="true" class="iconify" data-icon="icon-park-outline:setting-two"></i>
          </a>
        </li>
      </template>
    </MobileSidebar>

    <!-- Mobile subsidebar links -->
    <transition name="slide-x">
      <SettingsMobileSubsidebar v-if="isMobileSidebarOpen && activeMobileSubsidebar === 'settings'" />
    </transition>

    <!-- Desktop navigation -->
    <CircularMenu />

    <Sidebar :theme="props.theme" :is-open="isDesktopSidebarOpen">
      <template #links>
        <!-- Users -->
        <li v-if="isAdmin">
          <RouterLink id="users" :to="{ name: 'users' }" data-content="Users">
            <i aria-hidden="true" class="iconify sidebar-svg" data-icon="icon-park-outline:peoples"></i>
          </RouterLink>
        </li>

        <!-- Plans -->
        <li v-if="isAdmin">
          <RouterLink id="plans" :to="{ name: 'plans' }" data-content="Plans">
            <i aria-hidden="true" class="iconify sidebar-svg" data-icon="icon-park-outline:ad-product"></i>
          </RouterLink>
        </li>
      </template>

      <template #bottom-links>
        <!-- Settings -->
        <li v-if="isAdmin" class="is-hidden-touch">
          <a
            :class="[activeMobileSubsidebar === 'settings' && 'is-active']"
            data-content="Settings"
            aria-label="View Settings"
            tabindex="0"
            @keydown.space.prevent="switchSidebar('settings')"
            @click="switchSidebar('settings')"
          >
            <i aria-hidden="true" class="iconify sidebar-svg" data-icon="icon-park-outline:setting-two"></i>
          </a>
        </li>

        <!-- Profile Dropdown -->
        <li>
          <UserProfileDropdown up />
        </li>
      </template>
    </Sidebar>

    <Transition name="slide-x">
      <KeepAlive>
        <SettingsSubsidebar
          v-if="isDesktopSidebarOpen && activeMobileSubsidebar === 'settings'"
          @close="isDesktopSidebarOpen = false"
        />
      </KeepAlive>
    </Transition>

    <VViewWrapper>
      <VPageContentWrapper>
        <template v-if="props.nowrap">
          <slot></slot>
        </template>
        <VPageContent v-else class="is-relative">
          <div class="page-title has-text-centered">
            <!-- Sidebar Trigger -->
            <div
              class="vuer-hamburger nav-trigger push-resize"
              tabindex="0"
              @keydown.space.prevent="isDesktopSidebarOpen = !isDesktopSidebarOpen"
              @click="isDesktopSidebarOpen = !isDesktopSidebarOpen"
            >
              <span class="menu-toggle has-chevron">
                <span :class="[isDesktopSidebarOpen && 'active']" class="icon-box-toggle">
                  <span class="rotate">
                    <i aria-hidden="true" class="icon-line-top"></i>
                    <i aria-hidden="true" class="icon-line-center"></i>
                    <i aria-hidden="true" class="icon-line-bottom"></i>
                  </span>
                </span>
              </span>
            </div>

            <div class="title-wrap">
              <h1 class="title is-4">{{ viewWrapper.pageTitle }}</h1>
            </div>

            <Toolbar class="desktop-toolbar">
              <ToolbarNotification />

              <a class="toolbar-link right-panel-trigger" href="/admin/home">
                <i aria-hidden="true" class="iconify" data-icon="feather:grid"></i>
              </a>
            </Toolbar>
          </div>

          <slot></slot>
        </VPageContent>
      </VPageContentWrapper>
    </VViewWrapper>
  </div>
</template>
