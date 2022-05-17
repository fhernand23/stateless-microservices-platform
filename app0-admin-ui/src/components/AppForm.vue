<script setup lang="ts">
import { computed, ref, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWindowScroll } from '@vueuse/core'
import { useNotyf } from '/@src/composable/useNotyf'
import { onceImageErrored } from '/@src/utils/via-placeholder'
import { platformService } from '/@src/services/platformService'
import type { AppDef } from '/@src/models/platform'
import { ACT_APP_ARCHIVE, ACT_APP_UNARCHIVE } from '/@src/data/constants'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)
const notyf = useNotyf()
const { y } = useWindowScroll()
const theObj = ref<AppDef>({
  id: undefined,
  name: '',
  description: '',
  default_role: '',
  url: '',
})
const confirmArchiveApp = ref(false)
const confirmUnarchiveApp = ref(false)
const availableRoles = ref([])
const roleNames = computed(() => {
  return availableRoles.value ? availableRoles.value.map((e: any) => e.name) : []
})

const isStuck = computed(() => {
  return y.value > 30
})

const vErrors = ref({
  name: false,
  description: false,
  url: false,
  default_role: false,
})
const validateForm = () => {
  vErrors.value.name = !theObj.value.name
  vErrors.value.description = !theObj.value.description
  vErrors.value.url = !theObj.value.url
  vErrors.value.default_role = !theObj.value.default_role

  return !vErrors.value.description && !vErrors.value.name && !vErrors.value.url && !vErrors.value.default_role
}
const onSave = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const obj_r = await platformService.saveApp(theObj.value)
      theObj.value = obj_r

      notyf.success('Your changes have been successfully saved!')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onArchiveApp = async () => {
  isLoading.value = true
  try {
    await platformService.saveAppAction(theObj.value, ACT_APP_ARCHIVE)

    notyf.success('App has been archived')
    confirmArchiveApp.value = false
    router.push({ name: 'apps' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onUnarchiveApp = async () => {
  isLoading.value = true
  try {
    await platformService.saveAppAction(theObj.value, ACT_APP_UNARCHIVE)

    notyf.success('App has been unarchived')
    confirmUnarchiveApp.value = false
    router.push({ name: 'apps' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadApp = async () => {
  isLoading.value = true
  try {
    const objId = route.params.objId
    let ret = await platformService.getApp(objId)
    theObj.value = ret
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadRoles = async () => {
  try {
    const qry: any = { flts: {} }
    qry.flts['enabled'] = { eq_bool: true }
    let ret = await platformService.getRoles(qry)
    availableRoles.value = ret.results
  } catch (error: any) {
    notyf.error('Error loading roles: ' + error.message)
  }
}

const onAddImage = async (error: any, fileInfo: any) => {
  if (error) {
    console.error(error)
    return
  }
  const _file = fileInfo.file as File
  if (_file) {
    const formData = new FormData()
    formData.append('attachment', _file)

    try {
      const ret = await platformService.addLogo(formData)
      theObj.value.image = ret.filename
      const obj_r = await platformService.saveApp(theObj.value)
      theObj.value = obj_r

      notyf.info('File uploaded successfully')
    } catch (error: any) {
      notyf.error('Something was wrong: ' + error.message)
    }
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
    await loadApp()
  } else {
    theObj.value = {
      id: undefined,
      name: '',
      description: '',
      default_role: '',
      url: '',
    }
  }
  loadRoles()
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
        label: 'Apps',
        icon: 'icon-park-outline:all-application',
        to: { name: 'apps' },
      },
      {
        label: theObj.name,
        to: { name: 'app-edit', params: { objId: theObj.id } },
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
        label: 'Apps',
        icon: 'icon-park-outline:all-application',
        to: { name: 'apps' },
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
            <h3>App information</h3>
          </div>
          <div class="right">
            <div class="buttons">
              <VButton :to="{ name: 'apps' }" icon="lnir lnir-arrow-left rem-100" light raised elevated>
                Go Back
              </VButton>
              <VButton color="primary" :loading="isLoading" raised elevated @click="onSave"> Save Changes </VButton>
            </div>
          </div>
        </div>
      </div>
      <div class="form-body">
        <div class="form-section">
          <div class="columns is-multiline">
            <div class="column is-12">
              <VMessage color="warning"
                >WARNING: Making change in apps can affect apps functionality. If you are not sure about changes, don't
                do it.</VMessage
              >
            </div>

            <div class="column is-12">
              <VField>
                <label>* App Name</label>
                <VControl :has-error="vErrors.name">
                  <input v-model="theObj.name" type="text" class="input" />
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
                <label>* Url</label>
                <VControl :has-error="vErrors.url">
                  <input v-model="theObj.url" type="text" class="input" />
                  <p v-if="vErrors.url" class="help text-danger">Url is required</p>
                </VControl>
              </VField>
            </div>

            <div class="column is-12">
              <VField>
                <label>* Required role to access</label>
                <VControl :has-error="vErrors.default_role">
                  <Multiselect
                    v-model="theObj.default_role"
                    mode="single"
                    :options="roleNames"
                    placeholder="Role for specific app?"
                    :class="[vErrors.default_role && 'multiselect-error']"
                  />
                  <p v-if="vErrors.default_role" class="help text-danger">Required role is required</p>
                </VControl>
              </VField>
            </div>

            <div v-if="!isNew()" class="column is-6">
              <VField>
                <label>App preview</label>
              </VField>
              <div class="card-grid-item">
                <div class="card">
                  <div class="card-image">
                    <figure class="image is-16by9">
                      <img
                        v-if="theObj.image"
                        :src="platformService.getLogoURL(theObj.image)"
                        alt=""
                        @error.once="(event) => onceImageErrored(event, '1280x960')"
                      />
                      <img v-else src="" alt="" @error.once="(event) => onceImageErrored(event, '1280x960')" />
                    </figure>
                  </div>
                  <div class="card-content">
                    <div class="card-content-flex">
                      <div class="card-info">
                        <h3 class="dark-inverted">{{ theObj.description }}</h3>
                      </div>
                    </div>
                  </div>
                  <footer class="card-footer">
                    <a href="#" class="card-footer-item">Go</a>
                  </footer>
                </div>
              </div>
            </div>

            <div v-if="!isNew()" class="column is-6">
              <VField>
                <VControl v-tooltip="'Drop file here or Browse'">
                  <VFilePond
                    class="profile-filepond"
                    name="profile_filepond"
                    size="small"
                    :chunk-retry-delays="[500, 1000, 3000]"
                    label-idle="<i class='lnil lnil-cloud-upload'></i>"
                    :accepted-file-types="['image/png', 'image/jpeg', 'image/gif']"
                    :image-preview-height="140"
                    :image-resize-target-width="640"
                    :image-resize-target-height="480"
                    image-crop-aspect-ratio="1:1"
                    style-panel-layout="compact circle"
                    style-load-indicator-position="center bottom"
                    style-progress-indicator-position="center bottom"
                    style-button-remove-item-position="center bottom"
                    style-button-process-item-position="center bottom"
                    icon-remove="<i class='iconify' data-icon='feather:check-circle' aria-hidden='true'></i>"
                    @addfile="onAddImage"
                  />
                </VControl>
                <p>Upload App Image (Recommended size: 640x480)</p>
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
          <div v-if="theObj.enabled" class="column is-6">
            <VButton color="danger" raised :loading="isLoading" @click="confirmArchiveApp = true">
              Archive App
            </VButton>
          </div>
          <div v-if="!theObj.enabled" class="column is-6">
            <VButton color="info" raised :loading="isLoading" @click="confirmUnarchiveApp = true">
              Unarchive App
            </VButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  <VModal :open="confirmArchiveApp" title="Confirm action" size="small" @close="confirmArchiveApp = false">
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to archive the App from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onArchiveApp">Confirm</VButton>
    </template>
  </VModal>
  <VModal :open="confirmUnarchiveApp" title="Confirm action" size="small" @close="confirmUnarchiveApp = false">
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to unarchive the App from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onUnarchiveApp">Confirm</VButton>
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
