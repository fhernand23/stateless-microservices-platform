<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    items?: any[]
    squared?: boolean
  }>(),
  {
    items: () => [],
  }
)
</script>

<template>
  <div>
    <div v-for="(it, idx) in props.items" :key="idx" class="inner-list-item media-flex-center">
      <Logo :name1="it._id.label" />
      <div class="flex-meta is-light">
        <a href="#">{{ it._id.label }}</a>
      </div>
      <div class="flex-end">{{ it.count }}</div>
    </div>
  </div>
</template>

<style lang="scss">
.list-widget {
  .go-icon {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 36px;
    width: 36px;
    border-radius: var(--radius-rounded);
    background: var(--widget-grey);
    color: var(--light-text);

    &::before {
      content: attr(data-content);
      position: absolute;
      left: -45px;
      font-family: var(--font);
      font-size: 0.95rem;
      font-weight: 500;
    }

    &.is-squared {
      border-radius: 10px;
    }

    &.is-up {
      &::before {
        color: var(--green);
      }
    }

    &.is-down {
      &::before {
        color: var(--red);
      }
    }

    svg {
      height: 16px;
      width: 16px;
      stroke-width: 3px;
    }
  }
}

.is-dark {
  .list-widget {
    .go-icon {
      background: var(--dark-sidebar-light-3);
      border: 1px solid var(--dark-sidebar-light-12);
    }
  }
}
</style>
