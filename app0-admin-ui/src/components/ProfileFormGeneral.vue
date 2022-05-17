<script setup lang="ts">
import { computed } from 'vue'
import { useSession } from '/@src/stores/session'
import { useWindowScroll } from '@vueuse/core'
const session = useSession()

const { y } = useWindowScroll()

const isScrolling = computed(() => {
  return y.value > 30
})
</script>

<template>
  <div class="account-box is-form is-footerless">
    <div class="form-head stuck-header" :class="[isScrolling && 'is-stuck']">
      <div class="form-head-inner">
        <div class="left">
          <h3>General Info</h3>
        </div>
        <div class="right">
          <div class="buttons"></div>
        </div>
      </div>
    </div>
    <div class="form-body">
      <!--Fieldset-->
      <div class="fieldset">
        <div class="columns is-multiline">
          <div class="column is-12">
            <VField>
              <label>Name</label>
              <VControl icon="feather:user">
                <input :value="session.userData.fullname" type="text" class="input" placeholder="" disabled />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Email</label>
              <VControl icon="feather:mail">
                <input
                  v-model="session.userData.email"
                  type="email"
                  class="input"
                  placeholder=""
                  inputmode="email"
                  disabled
                />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>Phone Number</label>
              <VControl icon="feather:phone">
                <input
                  v-model="session.userData.phone_number"
                  type="tel"
                  class="input"
                  placeholder=""
                  inputmode="tel"
                  disabled
                />
              </VControl>
            </VField>
          </div>
          <div class="column is-12">
            <VField>
              <label>Address</label>
              <VControl icon="feather:map-pin">
                <input v-model="session.userData.address" type="text" class="input" placeholder="" disabled />
              </VControl>
            </VField>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
