<script setup lang="ts">
import { onUpdated, ref, useSlots } from 'vue'

export type VCardActionRadius = 'regular' | 'smooth' | 'rounded'
export interface VCardActionProps {
  title: string
  subtitle?: string
  avatar?: string
  badge?: string
  content?: string
  dataicon?: string
  radius?: VCardActionRadius
}

const props = withDefaults(defineProps<VCardActionProps>(), {
  subtitle: undefined,
  avatar: undefined,
  badge: undefined,
  content: undefined,
  dataicon: undefined,
  radius: 'regular',
})

const slots = useSlots()
const hasDefaultSlot = ref(!!slots.default?.())

onUpdated(() => {
  hasDefaultSlot.value = !!slots.default?.()
})
</script>

<template>
  <div
    class="is-raised"
    :class="[
      props.radius === 'regular' && 's-card',
      props.radius === 'smooth' && 'r-card',
      props.radius === 'rounded' && 'l-card',
    ]"
  >
    <div class="card-head">
      <VBlock :title="props.title" :subtitle="props.subtitle" center>
        <template #icon>
          <VIconBox v-if="props.dataicon" size="medium" color="warning" rounded>
            <i aria-hidden="true" class="iconify" :data-icon="props.dataicon"></i>
          </VIconBox>
          <VAvatar v-else :picture="props.avatar" :badge="props.badge" />
        </template>
        <template #action><slot name="action"></slot></template>
      </VBlock>
    </div>
    <div v-if="hasDefaultSlot" class="card-inner">
      <slot></slot>
    </div>
  </div>
</template>
