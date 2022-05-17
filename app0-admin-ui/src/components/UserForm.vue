<script setup lang="ts">
import { computed, ref, onBeforeMount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useWindowScroll } from '@vueuse/core'
import { useNotyf } from '/@src/composable/useNotyf'
import { platformService } from '/@src/services/platformService'
import type { User } from '/@src/models/platform'
import { ACT_USER_CREATE, ACT_USER_DELETE_USER, ACT_USERROLE_DELETE } from '/@src/data/constants'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)
const notyf = useNotyf()
const { y } = useWindowScroll()
const user = ref<User>({
  id: undefined,
  firstname: '',
  surname: '',
  username: '',
  email: '',
  phone_number: '',
  employee_id: '',
})
const confirmDeleteUser = ref(false)
const confirmAddRole = ref(false)
const confirmDeleteRole = ref(false)
const userRoles = ref([])
const availableRoles = ref([])

const isScrolling = computed(() => {
  return y.value > 30
})

const vErrors = ref({
  firstname: false,
  surname: false,
  email: false,
  phone_number: false,
  server_error_msg: '',
})
const validateForm = () => {
  vErrors.value.firstname = !user.value.firstname
  vErrors.value.surname = !user.value.surname
  vErrors.value.email = !user.value.email
  vErrors.value.phone_number = !user.value.phone_number

  return !vErrors.value.firstname && !vErrors.value.surname && !vErrors.value.email && !vErrors.value.phone_number
}
const onSave = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const user_r = await platformService.saveUser(user.value)
      user.value = user_r

      notyf.success('Your changes have been successfully saved!')
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onCreate = async () => {
  isLoading.value = true
  try {
    if (validateForm()) {
      const valid_email: any = await platformService.validateEmail(user.value.email)
      if (valid_email.id == 200) {
        vErrors.value.server_error_msg = ''
        user.value.username = user.value.email
        await platformService.saveUserAction(user.value, ACT_USER_CREATE)

        notyf.success('User has been created!')
        router.push({ name: 'users' })
      } else {
        vErrors.value.server_error_msg = valid_email.description
      }
    }
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const onDeleteUser = async () => {
  isLoading.value = true
  try {
    await platformService.saveUserAction(user.value, ACT_USER_DELETE_USER)

    notyf.success('User has been deleted')
    confirmDeleteUser.value = false
    router.push({ name: 'users' })
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadUser = async () => {
  isLoading.value = true
  try {
    const objId = route.params.objId
    let ret = await platformService.getUser(objId)
    user.value = ret
  } catch (error: any) {
    notyf.error(error.message)
  }
  isLoading.value = false
}

const loadUserRoles = async () => {
  try {
    if (user.value.username) {
      const qry: any = { flts: {} }
      qry.flts['username'] = { eq: user.value.username }
      let ret = await platformService.getUserRoles(qry)
      userRoles.value = ret.results
    }
  } catch (error: any) {
    notyf.error('Error loading roles: ' + error.message)
  }
}

const loadRoles = async () => {
  try {
    const qry: any = { flts: {} }
    qry.flts['enabled'] = { eq_bool: true }
    let ret = await platformService.getRoles(qry)
    availableRoles.value = ret.results
  } catch (error: any) {
    notyf.error('Error loading roles: ' + error.message)
  }
}
const userRoleNames = computed(() => {
  return userRoles.value ? userRoles.value.map((e: any) => e.role) : []
})
const filteredUserRoles: any = computed(() => {
  return userRoles.value
})
const filteredAvailableRoles: any = computed(() => {
  return availableRoles.value.filter((o: any) => {
    return !userRoleNames.value.includes(o.name)
  })
})
const tempAddRole = ref({
  name: '',
  description: '',
  application: '',
})
const tempDeleteRole = ref({
  id: undefined,
  username: '',
  role: '',
})
const popupDeleteRole = (obj: any) => {
  tempDeleteRole.value = obj
  confirmDeleteRole.value = true
}
const popupAddRole = (obj: any) => {
  tempAddRole.value = obj
  confirmAddRole.value = true
}
const onDeleteUserRole = async () => {
  try {
    await platformService.saveUserRoleAction(tempDeleteRole.value, ACT_USERROLE_DELETE)
    userRoles.value = userRoles.value.filter((ur: any) => {
      return !(ur.role === tempDeleteRole.value.role)
    })
  } catch (error: any) {
    notyf.error('Error deleting user role: ' + error.message)
  }
  confirmDeleteRole.value = false
}

const onAddUserRole = async () => {
  try {
    const userRole = {
      username: user.value.username,
      role: tempAddRole.value.name,
    }
    const userRole_r: any = await platformService.saveUserRole(userRole)
    userRoles.value.push(userRole_r)
  } catch (error: any) {
    notyf.error('Error adding user role: ' + error.message)
  }
  confirmAddRole.value = false
}

const isNew = () => {
  if (route.params.objId == 'new') {
    return true
  }
  return false
}

onBeforeMount(async () => {
  if (!isNew()) {
    await loadUser()
    loadUserRoles()
  } else {
    user.value = {
      id: undefined,
      firstname: '',
      surname: '',
      username: '',
      email: '',
      phone_number: '',
      employee_id: '',
    }
  }
  loadRoles()
})
</script>

<template>
  <div class="account-box is-form is-footerless">
    <div class="form-head stuck-header" :class="[isScrolling && 'is-stuck']">
      <div class="form-head-inner">
        <div class="left">
          <h3>General information</h3>
        </div>
        <div class="right">
          <div class="buttons">
            <VButton icon="lnir lnir-arrow-left rem-100" light raised elevated @click="$router.back()">
              Go Back
            </VButton>
            <VButton v-if="!isNew()" color="primary" raised elevated :loading="isLoading" @click="onSave">
              Save Changes
            </VButton>
            <VButton v-if="isNew()" color="primary" raised elevated :loading="isLoading" @click="onCreate">
              Create User
            </VButton>
          </div>
        </div>
      </div>
    </div>
    <div class="form-body">
      <div class="fieldset">
        <div class="columns is-multiline">
          <div class="column is-6">
            <VField>
              <label>* First Name</label>
              <VControl icon="feather:user" :has-error="vErrors.firstname">
                <input v-model="user.firstname" type="text" class="input" placeholder="" />
                <p v-if="vErrors.firstname" class="help text-danger">Firstname is required</p>
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <label>* Last Name</label>
              <VControl icon="feather:user" :has-error="vErrors.surname">
                <input v-model="user.surname" type="text" class="input" placeholder="" />
                <p v-if="vErrors.surname" class="help text-danger">Lastname is required</p>
              </VControl>
            </VField>
          </div>
          <div class="column is-12">
            <VField>
              <label>* Email</label>
              <VControl icon="feather:mail" :has-error="vErrors.email">
                <input v-model="user.email" type="email" class="input" placeholder="" inputmode="email" />
                <p v-if="vErrors.email" class="help text-danger">Email is required</p>
              </VControl>
            </VField>
            <VMessage v-if="vErrors.server_error_msg" color="danger">{{ vErrors.server_error_msg }}</VMessage>
          </div>
          <div class="column is-12">
            <VField>
              <label>* Phone Number</label>
              <VControl icon="feather:phone" :has-error="vErrors.phone_number">
                <input v-model="user.phone_number" type="text" class="input" placeholder="" />
                <p v-if="vErrors.phone_number" class="help text-danger">Phone Number is required</p>
              </VControl>
            </VField>
          </div>
        </div>
      </div>
      <div v-if="!isNew()" class="form-fieldset">
        <div class="fieldset-heading">
          <h4>Roles</h4>
        </div>
        <div class="columns is-multiline">
          <div class="column is-6">
            <h2 class="title is-6 is-narrow">Assigned roles</h2>
            <VMessage v-for="obj in filteredUserRoles" :key="obj.id">
              {{ obj.role }}
              <VIconButton
                v-tooltip="'Delete role from user'"
                color="danger"
                outlined
                circle
                icon="feather:x"
                @click="popupDeleteRole(obj)"
              />
            </VMessage>
          </div>
          <div class="column is-6">
            <h2 class="title is-6 is-narrow">Available roles</h2>
            <VMessage v-for="obj in filteredAvailableRoles" :key="obj">
              {{ obj.name }}
              <VIconButton
                v-tooltip="'Add role to user'"
                color="success"
                outlined
                circle
                icon="feather:plus"
                @click="popupAddRole(obj)"
              />
            </VMessage>
          </div>
        </div>
      </div>
      <div v-if="!isNew()" class="form-fieldset">
        <div class="fieldset-heading">
          <h4>Admin</h4>
        </div>
        <div class="columns is-multiline">
          <div class="column is-6">
            <VField>
              <VControl>
                <VSwitchBlock
                  v-model="user.company_representative"
                  color="success"
                  label="Company representative?"
                  disabled
                />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VField>
              <VControl>
                <VSwitchBlock v-model="user.enabled" color="success" label="User enabled?" />
              </VControl>
            </VField>
          </div>
          <div class="column is-6">
            <VButton color="danger" raised :loading="isLoading" @click="confirmDeleteUser = true">
              Delete User
            </VButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  <VModal :open="confirmDeleteUser" title="Confirm action" size="small" @close="confirmDeleteUser = false">
    <template #content>
      <VPlaceholderSection title="" subtitle="Are you sure to remove the user from the platform?" />
    </template>
    <template #action>
      <VButton color="danger" raised @click="onDeleteUser">Confirm</VButton>
    </template>
  </VModal>
  <VModal :open="confirmDeleteRole" title="Confirm action" size="small" @close="confirmDeleteRole = false">
    <template #content>
      <VPlaceholderSection title="" :subtitle="'Are you sure to Delete User Role: ' + tempDeleteRole.role" />
    </template>
    <template #action>
      <VButton color="primary" raised @click="onDeleteUserRole">Confirm</VButton>
    </template>
  </VModal>
  <VModal :open="confirmAddRole" title="Confirm action" size="small" @close="confirmAddRole = false">
    <template #content>
      <VPlaceholderSection title="" :subtitle="'Are you sure to Add User Role: ' + tempAddRole.name" />
    </template>
    <template #action>
      <VButton color="primary" raised @click="onAddUserRole">Confirm</VButton>
    </template>
  </VModal>
</template>
