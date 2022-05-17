<script setup lang="ts">
import { useRouter } from 'vue-router'

import { resetData } from '/@src/state/registrationWizardState'

const router = useRouter()

const regFinished = async () => {
  resetData()
  router.push({
    name: 'home',
  })
}
</script>

<template>
  <div class="step-content">
    <div class="step-title">
      <h2 class="dark-inverted">Congrats! You're all set.</h2>
      <p>Awesome, you just finished creating a user at this Platform.</p>
    </div>

    <div class="page-placeholder end-placeholder">
      <div class="placeholder-content">
        <img class="light-image" src="../assets/illustrations/wizard/finish.svg" alt="" />
        <img class="dark-image" src="../assets/illustrations/wizard/finish-dark.svg" alt="" />
        <h3>Get ready for next steps.</h3>
        <p>
          You have successfully created the user. Instructions to access the system and start using it have been sent to
          the email address entered.
        </p>
        <div class="button-wrap">
          <VButton color="primary" rounded bold elevated @click="regFinished"> Finish </VButton>
        </div>
      </div>
    </div>
  </div>
</template>
