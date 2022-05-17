<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import { utils } from '/@src/services/utils'
import { VAvatarSize } from './base/avatar/VAvatar.vue'
import { platformService } from '../services/platformService'

export type EntityType = 'employee' | 'insurance_company' | 'service_provider' | 'client'

export interface LogoProps {
  image?: string
  name1?: string
  name2?: string
  size?: VAvatarSize
  entity?: EntityType
  entityId?: string
}

const props = withDefaults(defineProps<LogoProps>(), {
  image: undefined,
  name1: undefined,
  name2: undefined,
  size: undefined,
  entity: undefined,
  entityId: undefined,
})

const image = ref('')

const getInitials = computed(() => {
  if (props.name1 && props.name2) {
    return utils.getInitials(props.name1 + ' ' + props.name2)
  } else if (props.name1) {
    return utils.getInitials(props.name1)
  }
  return ''
})

onBeforeMount(async () => {
  if (props.image) {
    image.value = props.image
  }
})
</script>

<template>
  <VAvatar v-if="!image" :initials="getInitials" :size="props.size" />
  <VAvatar v-if="image" :picture="platformService.getLogoURL(image)" :size="props.size" />
</template>
