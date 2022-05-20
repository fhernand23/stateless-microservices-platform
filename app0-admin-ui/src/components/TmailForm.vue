<script setup lang="ts">
import { useWindowScroll } from '@vueuse/core'
import { computed, ref, onBeforeMount } from 'vue'
import { useNotyf } from '/@src/composable/useNotyf'
import { platformService } from '/@src/services/platformService'
import { mailService } from '/@src/services/mailService'
import { useRoute } from 'vue-router'

const route = useRoute()
const isLoading = ref(false)
const notyf = useNotyf()
const { y } = useWindowScroll()
const theObj = ref({})
const testAddress = ref('')

const isStuck = computed(() => {
  return y.value > 30
})

const vErrors = ref({
  subject: false,
})
const validateForm = () => {
  vErrors.value.subject = !theObj.value.subject

  return !vErrors.value.subject
}
const onSave = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const obj_r = await platformService.saveTmail(theObj.value)
      theObj.value = obj_r

      notyf.success('Your changes have been successfully saved!')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onTest = async () => {
  isLoading.value = true
  try {
    if (testAddress.value) {
      const mail = {
        template: theObj.value.name,
        destinations: [testAddress.value],
        replacements: {},
        files: [],
      }
      await mailService.testTmail(mail)

      notyf.success('Mail sended!')
    } else {
      notyf.error('Enter an email destination')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadTmail = async () => {
  isLoading.value = true
  try {
    const objId = route.params.objId
    let ret = await platformService.getTmail(objId)
    theObj.value = ret
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

onBeforeMount(async () => {
  await loadTmail()
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
        label: 'Mails',
        icon: 'icon-park-outline:mail',
        to: { name: 'tmails' },
      },
      {
        label: theObj.name,
        to: { name: 'tmail-edit', params: { objId: theObj.id } },
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
        label: 'Mails',
        icon: 'icon-park-outline:mail',
        to: { name: 'tmails' },
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
            <h3>Mail template information</h3>
          </div>
          <div class="right">
            <div class="buttons">
              <VButton :to="{ name: 'tmails' }" icon="lnir lnir-arrow-left rem-100" light raised elevated>
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
            <div class="column is-6">
              <VField>
                <label>Template Name</label>
                <VControl>
                  <input v-model="theObj.name" type="text" class="input" disabled />
                </VControl>
              </VField>
            </div>

            <div class="column is-6">
              <VField>
                <label>Template File</label>
                <VControl>
                  <input v-model="theObj.template" type="text" class="input" disabled />
                </VControl>
              </VField>
            </div>

            <div class="column is-12">
              <VField>
                <label>Mail Description</label>
                <VControl>
                  <input v-model="theObj.description" type="text" class="input" />
                </VControl>
              </VField>
            </div>

            <div class="column is-12">
              <VField>
                <label>* Mail Subject</label>
                <VControl :has-error="vErrors.subject">
                  <input v-model="theObj.subject" type="text" class="input" />
                  <p v-if="vErrors.subject" class="help text-danger">Subject is required</p>
                </VControl>
              </VField>
            </div>
          </div>
        </div>

        <div class="form-section is-grey">
          <div class="form-section-header">
            <div class="left">
              <h3>Send a test mail</h3>
            </div>
            <div class="right">
              <!-- <VButton dark-outlined> Add People </VButton> -->
            </div>
          </div>

          <div class="form-section-inner">
            <div class="columns is-multiline">
              <div class="column is-12">
                <VField>
                  <label>Destination</label>
                  <VControl>
                    <input v-model="testAddress" type="text" class="input" placeholder="Enter a valid email address" />
                  </VControl>
                </VField>
                <VButton color="warning" raised @click="onTest"> Send a test email </VButton>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
@import '/@src/scss/abstracts/all';
@import '/@src/scss/components/forms-outer';

.form-layout {
  max-width: 740px;
  margin: 0 auto;
}
</style>
