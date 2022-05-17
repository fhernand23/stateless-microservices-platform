<script setup lang="ts">
import { registrationData, registrationValid } from '/@src/state/registrationWizardState'
</script>

<template>
  <div class="step-content">
    <div class="step-title">
      <h2 class="dark-inverted">User details</h2>
      <p>Complete the details related to user.</p>
    </div>

    <div class="project-info">
      <div class="project-info-head">
        <div class="project-info">
          <div class="project-name">
            <VField>
              <label>* Firstname</label>
              <VControl icon="feather:user" :has-error="registrationValid.firstname">
                <input v-model="registrationData.firstname" class="input" placeholder="* Firstname" />
                <p v-if="registrationValid.firstname" class="help text-danger">Firstname is required</p>
              </VControl>
            </VField>
          </div>
          <div class="project-name">
            <VField>
              <label>* Lastname</label>
              <VControl icon="feather:user" :has-error="registrationValid.surname">
                <input v-model="registrationData.surname" class="input" placeholder="* Lastname" />
                <p v-if="registrationValid.surname" class="help text-danger">Lastname is required</p>
              </VControl>
            </VField>
          </div>
          <div class="project-name">
            <VField>
              <label>* Email</label>
              <VControl icon="feather:mail" :has-error="registrationValid.email">
                <input v-model="registrationData.email" class="input" placeholder="* Email" />
                <p v-if="registrationValid.email" class="help text-danger">
                  Email is required and should be a valid email address
                </p>
              </VControl>
            </VField>
            <VMessage v-if="registrationValid.server_user_error_msg" color="danger">{{
              registrationValid.server_user_error_msg
            }}</VMessage>
          </div>
          <div class="project-name">
            <VField>
              <label>* Phone</label>
              <VControl icon="feather:phone" :has-error="registrationValid.phone">
                <input v-model="registrationData.phone" class="input" placeholder="* Mobile phone" />
                <p v-if="registrationValid.phone" class="help text-danger">
                  Mobile phone is required and should be a valid phone number
                </p>
              </VControl>
            </VField>
          </div>
          <div class="project-name">
            <VField>
              <label>* Address</label>
              <VControl icon="feather:map-pin" :has-error="registrationValid.address">
                <input v-model="registrationData.address" class="input" placeholder="Address" />
                <p v-if="registrationValid.address" class="help text-danger">Address is required</p>
              </VControl>
            </VField>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
