<script setup lang="ts">
import { computed, ref, onBeforeMount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useWindowScroll } from '@vueuse/core'
import { useNotyf } from '/@src/composable/useNotyf'
import { platformService } from '/@src/services/platformService'
import { optionsRegistrationStatus } from '/@src/data/options'
import { utils } from '/@src/services/utils'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)
const notyf = useNotyf()
const { y } = useWindowScroll()
const theObj = ref({})
const optsRegistrationStatus = optionsRegistrationStatus
const confirmDeleteRegistration = ref(false)

const isScrolling = computed(() => {
  return y.value > 30
})

const vErrors = ref({
  status: false,
})
const validateForm = () => {
  vErrors.value.status = !theObj.value.status

  return !vErrors.value.status
}
const onSave = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const obj_r = await platformService.saveRegistration(theObj.value)
      theObj.value = obj_r

      notyf.success('Your changes have been successfully saved!')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onDeleteRegistration = async () => {
  isLoading.value = true
  try {
    await platformService.saveRegistrationAction(theObj.value, 'ACT_REGISTRATION_DELETE')

    notyf.success('Registration has been deleted')
    confirmDeleteRegistration.value = false
    router.push({ name: 'registrations' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadRegistration = async () => {
  isLoading.value = true
  try {
    const objId = route.params.objId
    let ret = await platformService.getRegistration(objId)
    theObj.value = ret
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

onBeforeMount(async () => {
  await loadRegistration()
})
</script>

<template>
  <div class="account-box is-form is-footerless">
    <div class="form-head stuck-header" :class="[isScrolling && 'is-stuck']">
      <div class="form-head-inner">
        <div class="left">
          <h3>Information</h3>
        </div>
        <div class="right">
          <div class="buttons">
            <VButton :to="{ name: 'registrations' }" icon="lnir lnir-arrow-left rem-100" light raised elevated>
              Go Back
            </VButton>
            <VButton color="primary" raised elevated :loading="isLoading" @click="onSave"> Save Changes </VButton>
          </div>
        </div>
      </div>
    </div>
    <div class="form-body">
      <div class="fieldset">
        <div class="columns is-multiline">
          <div class="column is-6">
            <VField>
              <label>Creation Date</label>
              <VControl>
                <input
                  :value="utils.dateFmtStrH(theObj.creation_date)"
                  type="text"
                  class="input"
                  placeholder=""
                  disabled="true"
                />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Status</label>
              <VControl>
                <Multiselect
                  v-model="theObj.status"
                  mode="single"
                  :options="optsRegistrationStatus"
                  placeholder=""
                  :disabled="theObj.status == 'Confirmed'"
                />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>First Name</label>
              <VControl>
                <input v-model="theObj.firstname" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Last Name</label>
              <VControl>
                <input v-model="theObj.surname" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Email</label>
              <VControl>
                <input v-model="theObj.email" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Phone number</label>
              <VControl>
                <input v-model="theObj.phone" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Address</label>
              <VControl>
                <input v-model="theObj.address" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
        </div>
      </div>
      <!--Fieldset-->
      <div class="form-fieldset">
        <div class="fieldset-heading">
          <h4>Plan</h4>
        </div>
        <div class="columns is-multiline">
          <div class="column is-6">
            <VField>
              <label>Plan Id</label>
              <VControl>
                <input v-model="theObj.plan_id" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Plan Name</label>
              <VControl>
                <input v-model="theObj.plan_name" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
          <div class="column is-12">
            <VField>
              <label>Plan Description</label>
              <VControl>
                <input v-model="theObj.plan_description" type="text" class="input" placeholder="" />
              </VControl>
            </VField>
          </div>
        </div>
      </div>
      <!--Fieldset-->
      <div class="form-fieldset">
        <div class="fieldset-heading">
          <h4>Admin</h4>
        </div>
        <div class="columns is-multiline">
          <div class="column is-6">
            <VButton color="danger" raised :loading="isLoading" @click="confirmDeleteRegistration = true">
              Delete Registration
            </VButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  <VModal
    :open="confirmDeleteRegistration"
    title="Confirm action"
    size="small"
    @close="confirmDeleteRegistration = false"
  >
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to remove the registration from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onDeleteRegistration">Confirm</VButton>
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
