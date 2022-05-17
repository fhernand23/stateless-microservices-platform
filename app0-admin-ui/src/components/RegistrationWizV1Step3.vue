<script setup lang="ts">
import { registrationData, currentStep, isLoading } from '/@src/state/registrationWizardState'
</script>

<template>
  <div class="step-content">
    <div class="step-title">
      <h2 class="dark-inverted">Make sure everything is good</h2>
      <p>You can go back to previous steps if you need to edit anything.</p>
    </div>

    <VLoader size="xl" class="project-preview-wrapper" :active="isLoading" grey>
      <div class="project-preview-header">
        <h3 class="title is-4 is-narrow is-thin">
          <span>{{ registrationData.firstname + ' ' + registrationData.surname }}</span>

          <a class="edit-icon" @click="currentStep = 3">
            <i aria-hidden="true" class="lnil lnil-pencil"></i>
          </a>
        </h3>
      </div>

      <div class="project-preview-body">
        <div class="columns is-multiline">
          <div class="column is-12 is-tablet-100">
            <VCardActionc
              dataicon="icon-park-outline:application-one"
              :title="registrationData.plan_name"
              subtitle="Subscription Plan"
              radius="rounded"
            >
              <template #action>
                <a class="edit-icon" @click="currentStep = 1">
                  <i aria-hidden="true" class="lnil lnil-pencil"></i>
                </a>
              </template>
            </VCardActionc>
          </div>

          <div class="column is-12 is-tablet-100">
            <VCardActionc
              dataicon="icon-park-outline:user-business"
              :title="registrationData.firstname + ' ' + registrationData.surname"
              subtitle="Representative User"
              radius="rounded"
            >
              <template #action>
                <a class="edit-icon" @click="currentStep = 3">
                  <i aria-hidden="true" class="lnil lnil-pencil"></i>
                </a>
              </template>
              <VSnack :title="registrationData.email" color="info" icon="feather:mail"> </VSnack>
              <VSnack :title="registrationData.phone" color="info" icon="feather:phone"> </VSnack>
              <VSnack :title="registrationData.address" color="info" icon="feather:map-pin"> </VSnack>
            </VCardActionc>
          </div>
        </div>
      </div>
    </VLoader>
  </div>
</template>
