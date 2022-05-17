<script setup lang="ts">
import { useWindowScroll } from '@vueuse/core'
import { computed, ref, onBeforeMount } from 'vue'
import { useNotyf } from '/@src/composable/useNotyf'
import { platformService } from '/@src/services/platformService'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)
const notyf = useNotyf()
const { y } = useWindowScroll()
const theObj = ref({})
const confirmDeletePlan = ref(false)

const isScrolling = computed(() => {
  return y.value > 30
})

const vErrors = ref({
  name: false,
  subtitle: false,
})
const validateForm = () => {
  vErrors.value.name = !theObj.value.name
  vErrors.value.subtitle = !theObj.value.subtitle

  return !vErrors.value.name && !vErrors.value.subtitle
}
const onSave = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const obj_r = await platformService.savePlan(theObj.value)
      theObj.value = obj_r

      notyf.success('Your changes have been successfully saved!')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadPlan = async () => {
  isLoading.value = true
  try {
    const objId = route.params.objId
    let ret = await platformService.getPlan(objId)
    theObj.value = ret
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onAddLogo = async (error: any, fileInfo: any) => {
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
      const obj_r = await platformService.savePlan(theObj.value)
      theObj.value = obj_r

      notyf.info('File uploaded successfully')
    } catch (error: any) {
      console.log(error)
      notyf.error('Something was wrong: ' + error.message)
    }
  }
}

const onDeletePlan = async () => {
  isLoading.value = true
  try {
    await platformService.savePlanAction(theObj.value, 'ACT_PLAN_DELETE')

    notyf.success('Plan has been deleted')
    confirmDeletePlan.value = false
    router.push({ name: 'plans' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const isNew = () => {
  if (route.params.objId == 'new') {
    return true
  }
  return false
}

onBeforeMount(async () => {
  if (!isNew()) {
    await loadPlan()
  } else {
    theObj.value = {
      name: '',
      subtitle: '',
      description: '',
      learn_more_url: '',
      enabled: true,
    }
  }
})
</script>

<template>
  <div class="account-box is-form is-footerless">
    <div class="form-head stuck-header" :class="[isScrolling && 'is-stuck']">
      <div class="form-head-inner">
        <div class="left">
          <h3>Basic information</h3>
        </div>
        <div class="right">
          <div class="buttons">
            <VButton :to="{ name: 'plans' }" icon="lnir lnir-arrow-left rem-100" light raised elevated>
              Go Back
            </VButton>
            <VButton color="primary" :loading="isLoading" raised elevated @click="onSave"> Save Changes </VButton>
          </div>
        </div>
      </div>
    </div>
    <div class="form-body">
      <div class="fieldset">
        <div class="columns is-multiline">
          <div class="column is-6">
            <VField>
              <label>* Plan Name</label>
              <VControl icon="feather:package" :has-error="vErrors.name">
                <input v-model="theObj.name" type="text" class="input" placeholder="" />
                <p v-if="vErrors.name" class="help text-danger">Name is required</p>
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>* Subtitle</label>
              <VControl icon="feather:package" :has-error="vErrors.subtitle">
                <input v-model="theObj.subtitle" type="text" class="input" placeholder="" />
                <p v-if="vErrors.subtitle" class="help text-danger">Subtitle is required</p>
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Learn More URL</label>
              <VControl icon="feather:link">
                <input v-model="theObj.learn_more_url" type="text" class="input" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Contact URL</label>
              <VControl icon="feather:link">
                <input v-model="theObj.contact_url" type="text" class="input" />
              </VControl>
            </VField>
          </div>
          <div class="column is-12">
            <VField>
              <label>Description</label>
              <VControl>
                <textarea
                  v-model="theObj.description"
                  class="textarea"
                  rows="2"
                  placeholder=""
                  autocomplete="off"
                  autocapitalize="off"
                  spellcheck="false"
                ></textarea>
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Registration order</label>
              <VControl>
                <input
                  v-model.number="theObj.registration_order"
                  type="number"
                  class="input"
                  placeholder="Registration order"
                />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <VControl>
                <VSwitchBlock v-model="theObj.enabled" color="success" label="Active Plan" />
              </VControl>
            </VField>
          </div>
        </div>
      </div>
      <!--Fieldset-->
      <div class="form-fieldset">
        <div class="fieldset-heading">
          <h4>{{ theObj?.image ? 'Change Logo' : 'Add Logo' }}</h4>
        </div>
        <div class="columns is-multiline">
          <div class="column is-6">
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
                  :image-resize-target-width="140"
                  :image-resize-target-height="140"
                  image-crop-aspect-ratio="1:1"
                  style-panel-layout="compact circle"
                  style-load-indicator-position="center bottom"
                  style-progress-indicator-position="center bottom"
                  style-button-remove-item-position="center bottom"
                  style-button-process-item-position="center bottom"
                  icon-remove="<i class='iconify' data-icon='feather:check-circle' aria-hidden='true'></i>"
                  @addfile="onAddLogo"
                />
              </VControl>
            </VField>
          </div>
        </div>
      </div>

      <div v-if="!isNew()" class="form-fieldset">
        <div class="fieldset-heading">
          <h4>Admin</h4>
        </div>
        <div class="columns is-multiline">
          <div class="column is-6">
            <VButton color="danger" raised :loading="isLoading" @click="confirmDeletePlan = true">
              Delete Plan
            </VButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  <VModal :open="confirmDeletePlan" title="Confirm action" size="small" @close="confirmDeletePlan = false">
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to remove the plan from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onDeletePlan">Confirm</VButton>
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
