<script setup lang="ts">
import { computed, ref, onBeforeMount } from 'vue'
import { platformService } from '/@src/services/platformService'
import { useNotyf } from '/@src/composable/useNotyf'

const notyf = useNotyf()
const datalist = ref([])
const filters = ref('')

const filteredData: any = computed(() => {
  if (!filters.value) {
    return datalist.value
  } else {
    return datalist.value.filter((item: any) => {
      return item.name.match(new RegExp(filters.value, 'i'))
    })
  }
})

const loadRoles = async () => {
  try {
    const qry: any = { flts: {} }
    let ret = await platformService.getRoles(qry)
    datalist.value = ret.results
  } catch (error: any) {
    notyf.error(error.message)
  }
}

onBeforeMount(async () => {
  await loadRoles()
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
          label: 'Roles',
          icon: 'icon-park-outline:key',
          to: { name: 'roles' },
        },
      ]"
      with-icons
    />
    <VButtons align="right">
      <VButton :to="{ name: 'role-edit', params: { objId: 'new' } }" color="primary" icon="fas fa-plus" raised elevated>
        Add Role
      </VButton>
    </VButtons>
  </div>
  <div>
    <div class="tile-grid-toolbar">
      <VControl icon="feather:search">
        <input v-model="filters" class="input custom-text-filter" placeholder="Search..." />
      </VControl>
    </div>

    <div class="tile-grid tile-grid-v1">
      <!--List Empty Search Placeholder -->
      <VPlaceholderPage
        :class="[filteredData.length !== 0 && 'is-hidden']"
        title="We couldn't find any matching results."
        subtitle="Too bad. Looks like we couldn't find any matching results for the
          search terms you've entered. Please try different search terms or
          criteria."
        larger
      >
        <template #image>
          <img class="light-image" src="../assets/illustrations/placeholders/search-6.svg" alt="" />
          <img class="dark-image" src="../assets/illustrations/placeholders/search-6-dark.svg" alt="" />
        </template>
      </VPlaceholderPage>

      <!--Tile Grid v1-->
      <transition-group name="list" tag="div" class="columns is-multiline">
        <!--Grid item-->
        <div v-for="obj in filteredData" :key="obj.id" class="column is-4">
          <div class="tile-grid-item">
            <div class="tile-grid-item-inner">
              <RouterLink :to="{ name: 'role-edit', params: { objId: obj.id } }">
                <VIconBox size="medium" :color="obj.enabled ? 'primary' : 'danger'" rounded>
                  <i class="iconify" data-icon="icon-park-outline:key"></i>
                </VIconBox>
              </RouterLink>
              <div class="meta">
                <RouterLink :to="{ name: 'role-edit', params: { objId: obj.id } }">
                  <span class="dark-inverted">{{ obj.name }}</span>
                  <span> {{ obj.description }}</span>
                  <span><VTagc v-if="obj.application" :label="obj.application" color="purple" rounded outlined /></span>
                </RouterLink>
              </div>
              <VDropdown icon="feather:more-vertical" spaced right>
                <template #content>
                  <RouterLink :to="{ name: 'role-edit', params: { objId: obj.id } }">
                    <a role="menuitem" class="dropdown-item is-media">
                      <div class="icon">
                        <i aria-hidden="true" class="lnil lnil-pencil-alt"></i>
                      </div>
                      <div class="meta">
                        <span>Details</span>
                        <span>Edit information</span>
                      </div>
                    </a>
                  </RouterLink>
                </template>
              </VDropdown>
            </div>
          </div>
        </div>
      </transition-group>
    </div>
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

.is-dark {
  .tile-grid {
    .tile-grid-item {
      @include vuer-card--dark;
    }
  }
}

.tile-grid-v1 {
  .tile-grid-item {
    @include vuer-s-card;

    border-radius: 14px;
    padding: 16px;

    .tile-grid-item-inner {
      display: flex;
      align-items: center;

      .meta {
        margin-left: 10px;
        line-height: 1.2;

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
            color: var(--light-text);
            font-size: 0.9rem;
          }
        }
      }

      .dropdown {
        position: relative;
        margin-left: auto;
      }
    }
  }
}
</style>
