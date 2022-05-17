<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    items?: any[]
    rounded?: boolean
  }>(),
  {
    items: () => [],
  }
)
</script>

<template>
  <div>
    <div v-for="(it, idx) in props.items" :key="idx" class="inner-list-item media-flex-center">
      <VIconBox :rounded="props.rounded" color="info">
        <i aria-hidden="true" class="iconify" data-icon="feather:zap"></i>
      </VIconBox>
      <div class="flex-meta is-light">
        <a href="#">{{ it._id.label }}</a>
      </div>
      <div class="flex-end">
        {{ it.count }}
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.list-widget {
  .image-icon {
    height: 40px;
    width: 40px;
  }
}
</style>
