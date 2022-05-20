<script setup lang="ts">
import { computed, defineProps } from 'vue'
import { onceImageErrored } from '/@src/utils/via-placeholder'
import { platformService } from '../services/platformService'
import { utils } from '/@src/services/utils'

const props = defineProps({
  item: {
    type: Object,
    default: null,
  },
})

const getAmountDesc = computed(() => {
  return '$ ' + props.item.monthly_amount + ' monthly, ' + '$ ' + props.item.annual_amount + ' yearly'
})
</script>

<template>
  <RouterLink :to="{ name: 'plan-edit', params: { objId: item.id } }">
    <a class="card-grid-item">
      <img
        v-if="!item.image"
        src="../assets/icons/stacks/html5.svg"
        alt=""
        @error.once="(event) => onceImageErrored(event, '400x300')"
      />
      <img
        v-if="item.image"
        :src="platformService.getLogoURL(item.image)"
        alt=""
        @error.once="(event) => onceImageErrored(event, '400x300')"
      />
      <div class="card-grid-item-content">
        <h3 class="dark-inverted">{{ item.name }} <VTagc v-if="!item.enabled" color="warning" label="Disabled" /></h3>
      </div>
      <div class="card-grid-item-footer">
        <VAvatar :initials="utils.getInitials(item.name)" size="small" />
        <div class="meta">
          <span class="dark-inverted">{{ item.subtitle }}</span>
          <span>Order: {{ item.registration_order }} - {{ getAmountDesc }}</span>
        </div>
      </div>
    </a>
  </RouterLink>
</template>

<style lang="scss">
@import '/@src/scss/abstracts/all';

.card-grid {
  .columns {
    margin-left: -0.5rem !important;
    margin-right: -0.5rem !important;
    margin-top: -0.5rem !important;
  }

  .column {
    padding: 0.5rem !important;
  }
}

.card-grid-v4 {
  .card-grid-item {
    @include vuer-s-card;

    display: flex;
    flex-direction: column;
    padding: 10px;
    border-radius: 16px;
    min-height: 300px;

    &:hover,
    &:focus {
      box-shadow: var(--light-box-shadow);
    }

    > img {
      display: block;
      border-radius: 12px;
      width: 100%;
      height: 160px;
      object-fit: cover;
    }

    .card-grid-item-content {
      padding: 12px 5px;

      h3 {
        font-family: var(--font-alt);
        font-size: 1rem;
        font-weight: 600;
        color: var(--dark-text);
        line-height: 1.3;
      }
    }

    .card-grid-item-footer {
      display: flex;
      align-items: center;
      margin-top: auto;
      padding: 0 5px 10px;

      .meta {
        margin-left: 8px;
        line-height: 1.2;

        span {
          display: block;
          font-weight: 400;

          &:first-child {
            font-family: var(--font-alt);
            font-size: 0.9rem;
            color: var(--dark-text);
            font-weight: 600;
          }

          &:nth-child(2) {
            font-family: var(--font);
            font-size: 0.85rem;
            color: var(--light-text);
          }
        }
      }
    }
  }
}

.is-dark {
  .card-grid-v4 {
    .card-grid-item {
      @include vuer-card--dark;
    }
  }
}

@media only screen and (min-width: 768px) and (max-width: 1024px) and (orientation: portrait) {
  .card-grid-v4 {
    .columns {
      display: flex;
    }

    .column {
      width: 33.3%;
      min-width: 33.3%;
    }
  }
}
</style>
