<script setup lang="ts">
import { utils } from '/@src/services/utils'
import { companyUtils } from '/@src/services/companyUtils'
import { platformService } from '/@src/services/platformService'
import { useNotyf } from '/@src/composable/useNotyf'

const props = defineProps({
  companyId: {
    type: String,
    default: undefined,
  },
  item: {
    type: Object,
    default: undefined,
  },
})

const notyf = useNotyf()

const downloadFile = async () => {
  try {
    let fileBlob: Blob = await platformService.getCompanyFileBlob(props.companyId, props.item.file_resource.filename)
    const link = document.createElement('a')
    link.href = window.URL.createObjectURL(fileBlob)
    link.download = props.item.file_resource.src_filename ? props.item.file_resource.src_filename : 'file.pdf'
    link.target = '_blank'
    link.click()
  } catch (error: any) {
    notyf.error(error.message)
  }
}

const deleteFile = () => {
  notyf.info('Feature not yet implemented')
}
</script>

<template>
  <div class="tile-grid-item">
    <div class="tile-grid-item-inner">
      <img src="../../assets/icons/files/pdf.svg" alt="" />
      <div class="meta">
        <span class="dark-inverted">{{ companyUtils.getFileTypeDesc(props.item.tags) }}</span>
        <span>
          <span>{{ utils.strShort(props.item.file_resource?.src_filename) }}</span>
          <i aria-hidden="true" class="fas fa-circle icon-separator"></i>
          <span>{{ utils.humanFileSize(props.item.file_resource?.size) }}</span>
          <i aria-hidden="true" class="fas fa-circle icon-separator"></i>
          <span>{{ utils.dateFmtStrH(props.item.creation_date) }}</span>
        </span>
      </div>
      <VDropdown icon="feather:more-vertical" class="end-action" spaced right>
        <template #content>
          <a role="menuitem" href="#" class="dropdown-item is-media" @click="downloadFile()">
            <div class="icon">
              <i aria-hidden="true" class="lnil lnil-cloud-download"></i>
            </div>
            <div class="meta">
              <span>Download</span>
            </div>
          </a>
          <hr class="dropdown-divider" />
          <a role="menuitem" href="#" class="dropdown-item is-media" @click="deleteFile()">
            <div class="icon">
              <i aria-hidden="true" class="lnil lnil-trash-can-alt"></i>
            </div>
            <div class="meta">
              <span>Delete</span>
            </div>
          </a>
        </template>
      </VDropdown>
    </div>
  </div>
</template>
