<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  companyId: {
    type: String,
    default: undefined,
  },
  notifications: {
    type: Array,
    default: undefined,
  },
  types: {
    type: Array,
    default: undefined,
  },
})

const filteredNotifications = computed(() => {
  if (props.notifications) {
    if (props.types) {
      return props.notifications.filter((n) => {
        return props.types.includes(n.tags)
      })
    }
    return props.notifications
  }
  return []
})
</script>

<template>
  <div v-for="item in filteredNotifications" :key="item.id" class="column is-12">
    <CompanyFile :company-id="props.companyId" :item="item" />
  </div>
</template>

<style lang="scss">
@import '/@src/scss/abstracts/all';

.tile-grid {
  .columns {
    margin-left: -0.5rem !important;
    margin-right: -0.5rem !important;
    margin-top: -0.5rem !important;
  }

  .column {
    padding: 0.5rem !important;
  }
}

.tile-grid-v2 {
  .tile-grid-item {
    @include vuer-s-card();

    border-radius: 14px;
    padding: 16px;
    cursor: pointer;

    &:hover {
      border-color: var(--primary);
      box-shadow: var(--light-box-shadow);
    }

    .tile-grid-item-inner {
      display: flex;
      align-items: center;

      > img {
        display: block;
        width: 50px;
        height: 50px;
        min-width: 50px;
      }

      .meta {
        margin-left: 10px;
        line-height: 1.4;

        span {
          display: block;
          font-family: var(--font);

          &:first-child {
            color: var(--dark-text);
            font-family: var(--font-alt);
            font-weight: 600;
            font-size: 1rem;
          }

          &:nth-child(2) {
            display: flex;
            align-items: center;

            span {
              display: inline-block;
              color: var(--light-text);
              font-size: 0.8rem;
              font-weight: 400;
            }

            .icon-separator {
              position: relative;
              font-size: 4px;
              color: var(--light-text);
              padding: 0 6px;
            }
          }
        }
      }

      .dropdown {
        margin-left: auto;
      }
    }
  }
}

.is-dark {
  .tile-grid {
    .tile-grid-item {
      @include vuer-card--dark();
    }
  }

  .tile-grid-v2 {
    .tile-grid-item {
      @include vuer-card--dark();

      &:hover {
        border-color: var(--primary) !important;
      }
    }
  }
}
</style>
