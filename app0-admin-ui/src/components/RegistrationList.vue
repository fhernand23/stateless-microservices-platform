<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { platformService } from '/@src/services/platformService'
import { utils } from '/@src/services/utils'

const datalist = ref([])

onBeforeMount(async () => {
  const qry = {
    flts: {},
  }
  const res = await platformService.getRegistrations(qry)
  datalist.value = res.results
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
          label: 'Registrations',
          icon: 'icon-park-outline:clipboard',
          to: { name: 'registrations' },
        },
      ]"
      with-icons
    />
  </div>
  <VSimpleDatatables v-if="datalist.length > 0">
    <thead>
      <tr>
        <th scope="col">User</th>
        <th scope="col">Creation Date</th>
        <th scope="col">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(obj, index) in datalist" :key="index">
        <td>
          <div class="media-flex-center">
            <RouterLink :to="{ name: 'registration-edit', params: { objId: obj.id } }">
              <Logo :name1="obj.firstname" :name2="obj.surname" size="large" />
            </RouterLink>
            <RouterLink :to="{ name: 'registration-edit', params: { objId: obj.id } }">
              <div class="flex-meta">
                <span>{{ obj.firstname }} {{ obj.surname }}</span>
              </div>
            </RouterLink>
          </div>
        </td>
        <td>
          <span v-if="obj.creation_date" class="light-text">{{ utils.dateFmtStrH(obj.creation_date) }}</span>
        </td>
        <td>
          <span class="light-text">{{ obj.status }}</span>
        </td>
      </tr>
    </tbody>
  </VSimpleDatatables>
</template>
