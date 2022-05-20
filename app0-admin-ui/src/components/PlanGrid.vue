<script setup lang="ts">
import { computed, ref, onBeforeMount } from 'vue'
import { platformService } from '/@src/services/platformService'
import { useNotyf } from '/@src/composable/useNotyf'

const notyf = useNotyf()
const items = ref([])
const filters = ref('')
const isLoading = ref(false)

const filteredData: any = computed(() => {
  if (!filters.value) {
    return items.value
  } else {
    return items.value.filter((item: any) => {
      return item.name.match(new RegExp(filters.value, 'i'))
    })
  }
})

const loadPlans = async () => {
  isLoading.value = true
  try {
    const qry = {
      flts: {},
    }
    let ret = await platformService.getPlans(qry)
    items.value = ret.results
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

onBeforeMount(async () => {
  await loadPlans()
})
</script>

<template>
  <div class="list-view-toolbar">
    <VBreadcrumb
      :items="[
        {
          label: 'Home',
          hideLabel: true,
          icon: 'feather:home',
          to: { name: 'home' },
        },
        {
          label: 'Plans',
          icon: 'icon-park-outline:ad-product',
          to: { name: 'plans' },
        },
      ]"
      with-icons
    />
  </div>
  <div>
    <div class="card-grid-toolbar">
      <VControl icon="feather:search">
        <input v-model="filters" class="input custom-text-filter" placeholder="Search..." />
      </VControl>

      <div class="buttons">
        <VButtons align="right">
          <VButton :to="{ name: 'plan-edit', params: { objId: 'new' } }" color="primary" icon="fas fa-plus" elevated>
            Add Plan
          </VButton>
        </VButtons>
      </div>
    </div>

    <div class="card-grid card-grid-v4">
      <!--List Empty Search Placeholder -->
      <VPlaceholderPage
        v-if="!isLoading"
        :class="[filteredData.length !== 0 && 'is-hidden']"
        title="We couldn't find any matching results."
        subtitle="Too bad. Looks like we couldn't find any matching results for the
          search terms you've entered. Please try different search terms or
          criteria."
        larger
      >
        <template #image>
          <img class="light-image" src="../assets/illustrations/placeholders/search-4.svg" alt="" />
          <img class="dark-image" src="../assets/illustrations/placeholders/search-4-dark.svg" alt="" />
        </template>
      </VPlaceholderPage>

      <transition-group name="list" tag="div" class="columns is-multiline">
        <!--Grid item-->
        <div v-for="item in filteredData" :key="item.id" class="column is-3">
          <Plan :item="item" />
        </div>
      </transition-group>
    </div>
  </div>
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
