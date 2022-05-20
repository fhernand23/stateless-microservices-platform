<script setup lang="ts">
import { computed, ref, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWindowScroll } from '@vueuse/core'
import { useNotyf } from '/@src/composable/useNotyf'
import { platformService } from '/@src/services/platformService'
import type { AppRole } from '/@src/models/platform'
import { ACT_ROLE_ARCHIVE, ACT_ROLE_UNARCHIVE } from '/@src/data/constants'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)
const notyf = useNotyf()
const { y } = useWindowScroll()
const theObj = ref<AppRole>({
  id: undefined,
  name: '',
  description: '',
  can_delete: true,
})
const confirmArchiveRole = ref(false)
const confirmUnarchiveRole = ref(false)
const availableApps = ref([])
const appNames = computed(() => {
  return availableApps.value ? availableApps.value.map((e: any) => e.name) : []
})

const isStuck = computed(() => {
  return y.value > 30
})

const vErrors = ref({
  name: false,
  description: false,
})
const validateForm = () => {
  vErrors.value.name = !theObj.value.name
  vErrors.value.description = !theObj.value.description

  return !vErrors.value.description && !vErrors.value.name
}
const onSave = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const obj_r = await platformService.saveRole(theObj.value)
      theObj.value = obj_r

      notyf.success('Your changes have been successfully saved!')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onArchiveRole = async () => {
  isLoading.value = true
  try {
    await platformService.saveRoleAction(theObj.value, ACT_ROLE_ARCHIVE)

    notyf.success('Role has been archived')
    confirmArchiveRole.value = false
    router.push({ name: 'roles' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onUnarchiveRole = async () => {
  isLoading.value = true
  try {
    await platformService.saveRoleAction(theObj.value, ACT_ROLE_UNARCHIVE)

    notyf.success('Role has been unarchived')
    confirmUnarchiveRole.value = false
    router.push({ name: 'roles' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadRole = async () => {
  isLoading.value = true
  try {
    const objId = route.params.objId
    let ret = await platformService.getRole(objId)
    theObj.value = ret
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadApps = async () => {
  try {
    const qry: any = { flts: {} }
    qry.flts['enabled'] = { eq_bool: true }
    let ret = await platformService.getApps(qry)
    availableApps.value = ret.results
  } catch (error: any) {
    notyf.error('Error loading apps: ' + error.message)
  }
}

const isNew = () => {
  if (route.params.objId == 'new') {
    return true
  }
  return false
}

onBeforeMount(async () => {
  if (!isNew()) {
    await loadRole()
  } else {
    theObj.value = {
      id: undefined,
      name: '',
      description: '',
      can_delete: true,
    }
  }
  loadApps()
})
</script>

<template>
  <VBreadcrumb
    v-if="theObj.id"
    :items="[
      {
        label: 'Home',
        hideLabel: true,
        icon: 'feather:home',
        to: { name: 'home' },
      },
      {
        label: 'Roles',
        icon: 'icon-park-outline:key',
        to: { name: 'roles' },
      },
      {
        label: theObj.name,
        to: { name: 'role-edit', params: { objId: theObj.id } },
      },
    ]"
    with-icons
  />
  <VBreadcrumb
    v-if="theObj && !theObj.id"
    :items="[
      {
        label: 'Home',
        hideLabel: true,
        icon: 'feather:home',
        to: { name: 'home' },
      },
      {
        label: 'Roles',
        icon: 'icon-park-outline:key',
        to: { name: 'roles' },
      },
      {
        label: 'New',
      },
    ]"
    with-icons
  />
  <div class="form-layout is-stacked">
    <div class="form-outer">
      <div :class="[isStuck && 'is-stuck']" class="form-header stuck-header">
        <div class="form-header-inner">
          <div class="left">
            <h3>Role information</h3>
          </div>
          <div class="right">
            <div class="buttons">
              <VButton :to="{ name: 'roles' }" icon="lnir lnir-arrow-left rem-100" light raised elevated>
                Go Back
              </VButton>
              <VButton color="primary" raised elevated :loading="isLoading" @click="onSave"> Save Changes </VButton>
            </div>
          </div>
        </div>
      </div>
      <div class="form-body">
        <div class="form-section">
          <div class="columns is-multiline">
            <div class="column is-12">
              <VMessage color="warning"
                >WARNING: Making change in roles can affect apps functionality. If you are not sure about changes, don't
                do it.</VMessage
              >
            </div>

            <div class="column is-12">
              <VField>
                <label>* Role Name</label>
                <VControl :has-error="vErrors.name">
                  <input v-model="theObj.name" type="text" class="input" :disabled="!theObj.can_delete" />
                  <p v-if="vErrors.name" class="help text-danger">Name is required</p>
                </VControl>
              </VField>
            </div>

            <div class="column is-12">
              <VField>
                <label>* Description</label>
                <VControl :has-error="vErrors.description">
                  <input v-model="theObj.description" type="text" class="input" />
                  <p v-if="vErrors.description" class="help text-danger">Description is required</p>
                </VControl>
              </VField>
            </div>

            <div class="column is-12">
              <VField>
                <label>Application</label>
                <VControl>
                  <Multiselect
                    v-model="theObj.application"
                    mode="single"
                    :options="appNames"
                    placeholder="Role for specific app?"
                  />
                </VControl>
              </VField>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!isNew()" class="form-fieldset">
        <div class="fieldset-heading">
          <h4>Admin</h4>
        </div>
        <div class="columns is-multiline">
          <div v-if="!theObj.can_delete" class="column is-12">
            <VMessage color="warning">Required platform Role. This can't be deleted or archived.</VMessage>
          </div>
          <div v-if="!theObj.enabled" class="column is-12">
            <VMessage color="warning">Role is not enabled.</VMessage>
          </div>
          <div v-if="theObj.enabled" class="column is-12">
            <VMessage color="info">Role is enabled.</VMessage>
          </div>
          <div v-if="theObj.can_delete && theObj.enabled" class="column is-6">
            <VButton color="danger" raised :loading="isLoading" @click="confirmArchiveRole = true">
              Archive Role
            </VButton>
          </div>
          <div v-if="theObj.can_delete && !theObj.enabled" class="column is-6">
            <VButton color="info" raised :loading="isLoading" @click="confirmUnarchiveRole = true">
              Unarchive Role
            </VButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  <VModal :open="confirmArchiveRole" title="Confirm action" size="small" @close="confirmArchiveRole = false">
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to archive the role from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onArchiveRole">Confirm</VButton>
    </template>
  </VModal>
  <VModal :open="confirmUnarchiveRole" title="Confirm action" size="small" @close="confirmUnarchiveRole = false">
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to unarchive the role from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onUnarchiveRole">Confirm</VButton>
    </template>
  </VModal>
</template>

<style lang="scss">
@import '/@src/scss/abstracts/all';
@import '/@src/scss/components/forms-outer';

.form-layout {
  max-width: 740px;
  margin: 0 auto;
}
</style>
