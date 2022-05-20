<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { registrationData, currentStep } from '/@src/state/registrationWizardState'
import { publicService } from '/@src/services/publicService'

const items = ref([])
// const payment_by_year = ref(true)
const selectPlan = (selectedPlanId) => {
  const plan = items.value.filter((i) => i.id == selectedPlanId)
  // fill plan details
  // registrationData.relatedTo = relatedTo
  registrationData.plan_id = plan[0].id
  registrationData.plan_name = plan[0].name
  registrationData.plan_description = plan[0].description

  currentStep.value = 2
}
onBeforeMount(async () => {
  let ret = await publicService.getEnabledPlans()
  console.log(ret.results)
  items.value = ret.results
})
</script>

<template>
  <div class="step-content">
    <div class="step-title">
      <h2 class="dark-inverted">Select a Plan</h2>
    </div>

    <div class="wizard-types">
      <div class="columns">
        <div v-for="item in items" :key="item" class="column is-4">
          <div class="wizard-card">
            <img v-if="item.image" :src="publicService.getLogoURL(item.image)" alt="" />
            <img v-else src="../assets/illustrations/wizard/type-2.svg" alt="" />
            <h3 class="dark-inverted">{{ item.name }}</h3>
            <p>{{ item.subtitle }}</p>
            <!-- free plan -->
            <h1 class="title is-3 is-narrow is-bold card-price">Free</h1>
            <template v-if="item.contact_url">
              <!-- contact us plan -->
              <h1 class="title is-3 is-narrow is-bold card-price">Contact</h1>
            </template>
            <div class="content">
              <ul>
                <li v-if="item.description">{{ item.description }}</li>
              </ul>
            </div>
            <div class="button-wrap">
              <VButton color="primary" class="type-select-button" rounded elevated bold @click="selectPlan(item.id)">
                Select
              </VButton>
            </div>
            <div v-if="item.learn_more_url" class="learn-more-link">
              <a :href="item.learn_more_url" target="_blank" class="dark-inverted-hover">Or Learn More</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '/@src/scss/abstracts/all';

.card-price {
  color: var(--primary) !important;
}
</style>
