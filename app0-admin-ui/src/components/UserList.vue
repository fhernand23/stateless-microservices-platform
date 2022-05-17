<script setup lang="ts">
import { ref, onBeforeMount, computed, watch } from 'vue'
import { platformService } from '/@src/services/platformService'
import { useRoute } from 'vue-router'

const route = useRoute()
const datalist = ref([])

const currentPage = computed(() => {
  try {
    return Number.parseInt(route.query.page as string) || 1
  } catch {}
  return 1
})
const pageSize = ref(10)
const searchText = ref('')
const pagination = ref({})

const getData = async () => {
  // const qry: any = {
  //   flts: searchText.value ? { text: { text: searchText.value } } : {},
  // }
  const qry: any = { flts: {} }
  qry.flts['enabled'] = { eq_bool: true }
  if (searchText.value) {
    qry.flts['or_regex'] = {
      or_regex: {
        username: searchText.value,
        firstname: searchText.value,
        surname: searchText.value,
        email: searchText.value,
        phone_number: searchText.value,
      },
    }
  }
  const res = await platformService.getUsers(qry, currentPage.value, pageSize.value)

  pagination.value = {
    page: res.page,
    page_size: res.page_size,
    total: res.total,
  }
  datalist.value = res.results
}

watch(currentPage, async () => {
  await getData()
})

onBeforeMount(async () => {
  await getData()
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
          label: 'Users',
          icon: 'icon-park-outline:peoples',
          to: { name: 'users' },
        },
      ]"
      with-icons
    />
  </div>
  <div class="list-flex-toolbar flex-list-v1">
    <VField addons>
      <VControl expanded>
        <input v-model="searchText" type="text" class="input" placeholder="Search..." @keyup.enter="getData" />
      </VControl>
      <VControl>
        <VButton color="info" icon="fas fa-search" raised elevated @click="getData"> Search </VButton>
      </VControl>
    </VField>

    <VButtons align="right">
      <VButton :to="{ name: 'user-edit', params: { objId: 'new' } }" color="primary" icon="fas fa-plus" raised elevated>
        Add Platform User
      </VButton>
    </VButtons>
  </div>

  <div class="dataTable-wrapper dataTable-loading no-footer sortable searchable fixed-columns">
    <div class="dataTable-container">
      <table v-if="datalist.length > 0" class="dataTable-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Name</th>
            <th>E-mail</th>
            <th>Phone</th>
            <th>Company</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(obj, index) in datalist" :key="index">
            <td>
              <div class="media-flex-center">
                <RouterLink :to="{ name: 'user-edit', params: { objId: obj.id } }">
                  <Logo :image="obj.image" :name1="obj.firstname" :name2="obj.surname" size="medium" />
                </RouterLink>
                <RouterLink :to="{ name: 'user-edit', params: { objId: obj.id } }">
                  <div class="flex-meta">
                    <span>{{ obj.username }}</span>
                  </div>
                </RouterLink>
              </div>
            </td>
            <td>
              <span class="light-text">{{ obj.firstname }} {{ obj.surname }}</span>
            </td>
            <td>
              <span class="light-text">{{ obj.email }}</span>
            </td>
            <td>
              <span class="light-text">{{ obj.phone_number }}</span>
            </td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <VFlexPagination
    v-if="pagination.total"
    :item-per-page="pageSize"
    :total-items="pagination.total"
    :max-links-displayed="10"
    :current-page="currentPage"
  />

  <span v-if="pagination.total == 0">No match found</span>
</template>

<style lang="scss">
@import '/@src/scss/abstracts/all';

.is-navbar {
  .datatable-toolbar {
    padding-top: 30px;
  }
}

.datatable-toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;

  &.is-reversed {
    flex-direction: row-reverse;
  }

  .field {
    margin-bottom: 0;

    .control {
      .button {
        color: var(--light-text);

        &:hover,
        &:focus {
          background: var(--primary);
          border-color: var(--primary);
          color: var(--primary--color-invert);
        }
      }
    }
  }

  .buttons {
    margin-left: auto;
    margin-bottom: 0;

    .v-button {
      margin-bottom: 0;
    }
  }
}

.is-dark {
  .datatable-toolbar {
    .field {
      .control {
        .button {
          background: var(--dark-sidebar) !important;
          color: var(--light-text);

          &:hover,
          &:focus {
            background: var(--primary) !important;
            border-color: var(--primary) !important;
            color: var(--smoke-white) !important;
          }
        }
      }
    }
  }
}

.dataTable-wrapper {
  .dataTable-top {
    margin-bottom: 1.5rem;
    padding-left: 0;
    padding-right: 0;

    .dataTable-dropdown {
      label {
        display: block;
        position: relative;
        font-family: var(--font);
        font-weight: 400;
        font-size: 0.9rem;
        color: var(--light-text);

        &::after {
          position: absolute;
          top: 1px;
          right: 4px;
          content: '';
          font-family: 'Font Awesome 5 Free';
          font-weight: 900;
          font-size: 0.9rem;
          color: var(--light-text);
          height: 36px;
          width: 36px;
          border-radius: 0.5rem;
          display: flex;
          justify-content: center;
          align-items: center;
          background: var(--white);
        }
      }

      select {
        font-size: 1rem;
        background: var(--white);
        border: 1px solid var(--border);
        color: var(--dark-text);
        border-radius: 0.5rem;
        height: 38px;
        transition: box-shadow 0.3s;

        &:focus {
          box-shadow: var(--light-box-shadow);
        }
      }
    }

    .dataTable-search {
      position: relative;

      &::after {
        position: absolute;
        top: 1px;
        right: 4px;
        content: '\f002';
        font-family: 'Font Awesome 5 Free';
        font-weight: 900;
        font-size: 0.9rem;
        color: var(--light-text);
        height: 36px;
        width: 36px;
        border-radius: 0.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        background: var(--white);
      }

      input {
        font-family: var(--font);
        font-size: 1rem;
        background: var(--white);
        border: 1px solid var(--border);
        color: var(--dark-text);
        border-radius: 0.5rem;
        height: 38px;
        transition: box-shadow 0.3s;

        &::placeholder {
          color: var(--placeholder);
        }

        &:focus {
          box-shadow: var(--light-box-shadow);
        }
      }
    }
  }

  .dataTable-container {
    background: var(--white);
    border: none !important;
    overflow-x: auto;

    &::-webkit-scrollbar {
      height: 8px !important;
    }

    &::-webkit-scrollbar-thumb {
      border-radius: 10px !important;
      background: rgb(0 0 0 / 20%) !important;
    }

    .dataTable-table {
      border: 1px solid var(--fade-grey);
      border-collapse: collapse;
      border-radius: 0.75rem;
      // newken-devs customization start
      max-width: 100%;
      width: 100%;
      border-spacing: 0;
      // newken-devs end

      th {
        padding: 16px 20px;
        font-family: var(--font-alt);
        font-size: 0.8rem;
        color: var(--dark-text);
        text-transform: uppercase;
        border: 1px solid var(--fade-grey);
        font-weight: 600;

        &:last-child {
          text-align: right;
        }
      }

      td {
        font-family: var(--font);
        vertical-align: middle;
        padding: 12px 20px;
        border-bottom: 1px solid var(--fade-grey);

        &:last-child {
          text-align: right;
        }

        &.dataTables-empty {
          opacity: 0;
        }
      }

      .light-text {
        color: var(--light-text);
      }

      .flex-media {
        display: flex;
        align-items: center;

        .meta {
          margin-left: 10px;
          line-height: 1.3;

          span {
            display: block;
            font-size: 0.8rem;
            color: var(--light-text);
            font-family: var(--font);

            &:first-child {
              font-family: var(--font-alt);
              color: var(--dark-text);
            }
          }
        }
      }

      .row-action {
        display: flex;
        justify-content: flex-end;
      }

      .checkbox {
        padding: 0;
      }

      .product-photo {
        width: 80px;
        height: 80px;
        object-fit: contain;
      }

      .file-icon {
        width: 46px;
        height: 46px;
        object-fit: contain;
      }

      .drinks-icon {
        display: block;
        max-width: 48px;
        border-radius: var(--radius-rounded);
        border: 1px solid var(--fade-grey);
      }

      .negative-icon,
      .positive-icon {
        svg {
          height: 16px;
          width: 16px;
        }
      }

      .positive-icon {
        .iconify {
          color: var(--success);

          * {
            stroke-width: 4px;
          }
        }
      }

      .negative-icon {
        &.is-danger {
          .iconify {
            color: var(--danger) !important;
          }
        }

        .iconify {
          color: var(--light-text);

          * {
            stroke-width: 4px;
          }
        }
      }

      .price {
        color: var(--dark-text);
        font-weight: 500;

        &::before {
          content: '$';
        }

        &.price-free {
          color: var(--light-text);
        }
      }

      .status {
        display: flex;
        align-items: center;

        &.is-available {
          i {
            color: var(--success);
          }
        }

        &.is-busy {
          i {
            color: var(--danger);
          }
        }

        &.is-offline {
          i {
            color: var(--light-text);
          }
        }

        i {
          margin-right: 8px;
          font-size: 8px;
        }

        span {
          font-family: var(--font);
          font-size: 0.9rem;
          color: var(--light-text);
        }
      }
    }
  }

  .dataTable-bottom {
    .dataTable-info {
      font-family: var(--font);
      font-size: 0.9rem;
      color: var(--light-text);
    }

    .dataTable-pagination {
      li {
        &:not(.active) {
          a:hover {
            background: var(--white);
          }
        }

        &.active {
          a {
            background: var(--primary);
            box-shadow: var(--primary-box-shadow);
            color: var(--primary--color-invert);
          }
        }

        a {
          display: flex;
          justify-content: center;
          align-items: center;
          font-family: var(--font);
          color: var(--light-text);
          border-radius: var(--radius-rounded);
          min-width: 34px;
          min-height: 34px;
          padding: 0;
        }
      }
    }
  }
}

.is-dark {
  .dataTable-wrapper {
    .dataTable-top {
      .dataTable-dropdown {
        label {
          &::after {
            background: var(--dark-sidebar-light-6) !important;
          }
        }

        select {
          border-color: var(--dark-sidebar-light-12);
          background: var(--dark-sidebar-light-6);
          color: var(--white);
        }
      }

      .dataTable-search {
        &::after {
          background: var(--dark-sidebar-light-6) !important;
        }

        input {
          border-color: var(--dark-sidebar-light-12);
          background: var(--dark-sidebar-light-6);
          color: var(--white);
        }
      }
    }

    .dataTable-container {
      border-color: var(--dark-sidebar-light-12);
      background: var(--dark-sidebar-light-6);

      .dataTable-table {
        border-color: var(--dark-sidebar-light-12);

        th,
        td {
          border-color: var(--dark-sidebar-light-12);
          color: var(--dark-dark-text);
        }

        th {
          .dataTable-sorter {
            &::before {
              border-top-color: var(--dark-dark-text);
            }

            &::after {
              border-bottom-color: var(--dark-dark-text);
            }
          }
        }

        .drinks-icon {
          border-color: var(--dark-sidebar-light-12);
        }
      }
    }
  }
}
</style>
