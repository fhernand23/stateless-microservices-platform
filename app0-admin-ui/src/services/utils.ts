import dayjs from 'dayjs'

export const utils = {
  getInitials(str: string) {
    if (str) {
      const words_array = str.split(' ')
      let inits = ''
      if (words_array.length > 1) inits = words_array.map((word) => word[0]).join('')
      else inits = str.substring(0, 2)

      if (inits.length > 3) return inits.substring(0, 3).toUpperCase()

      return inits.toUpperCase()
    }
    return ''
  },
  // https://day.js.org/docs/en/display/format
  dateFormat(the_date: any) {
    return the_date ? dayjs(the_date).format('MM/DD/YYYY') : ''
  },
  dateFmt(the_date: any, mask: string) {
    return the_date ? dayjs(the_date).format(mask) : ''
  },
  dateFmtStr(the_date: any) {
    return the_date ? dayjs(the_date).format('MMMM D, YYYY') : ''
  },
  dateFmtStrH(the_date: any) {
    return the_date ? dayjs(the_date).format('MMMM D, YYYY H:mm') : ''
  },
  dateFmtMdyh(the_date: any) {
    return the_date ? dayjs(the_date).format('MM/DD/YYYY H:mm') : ''
  },
  dateYMDHm(the_date: any) {
    return the_date ? dayjs(the_date).format('YYYY/MM/DD H:mm') : ''
  },
  getIsoCurrentDateTime() {
    const now = dayjs()
    return dayjs(now).toISOString()
  },
  /**
   * Format bytes as human-readable text.
   *
   * @param bytes Number of bytes.
   * @param si True to use metric (SI) units, aka powers of 1000. False to use
   *           binary (IEC), aka powers of 1024.
   * @param dp Number of decimal places to display.
   *
   * @return Formatted string.
   */
  humanFileSize(bytes: number, si: boolean = true, dp: number = 1) {
    const thresh = si ? 1000 : 1024

    if (Math.abs(bytes) < thresh) {
      return bytes + ' B'
    }

    const units = si
      ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
      : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    let u = -1
    const r = 10 ** dp

    do {
      bytes /= thresh
      ++u
    } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1)

    return bytes.toFixed(dp) + ' ' + units[u]
  },
  strShort(str: string, max: number = 15) {
    if (str) {
      return str.length <= max ? str : str.substring(0, max) + '...'
    }

    return ''
  },
  getNotificationImage(str: string) {
    let ret = 'icon-park-outline:info'
    if (str === 'error') {
      ret = 'icon-park-outline:caution'
    } else if (str === 'direct') {
      ret = 'icon-park-outline:message'
    } else if (str === 'upload') {
      ret = 'icon-park-outline:paperclip'
    } else if (str === 'mail') {
      ret = 'icon-park-outline:mail'
    } else if (str === 'call') {
      ret = 'feather:phone-call'
    } else if (str === 'papers') {
      ret = 'icon-park-outline:folder'
    } else if (str === 'event') {
      ret = 'icon-park-outline:calendar'
    } else if (str === 'state-change') {
      ret = 'icon-park-outline:refresh-one'
    } else if (str === 'estimation') {
      ret = 'icon-park-outline:chart-line'
    } else if (str === 'negotiation') {
      ret = 'icon-park-outline:imbalance'
    } else if (str === 'agreement') {
      ret = 'icon-park-outline:thumbs-up'
    } else if (str === 'decline') {
      ret = 'icon-park-outline:thumbs-down'
    }

    return ret
  },
  getNotificationColor(str: string) {
    let ret = 'blue'
    if (str === 'decline' || str === 'error') {
      ret = 'red'
    } else if (str === 'agreement') {
      ret = 'green'
    } else if (str === 'state-change') {
      ret = 'orange'
    } else if (str === 'event') {
      ret = 'purple'
    }
    return ret
  },
  getNotificationObjectDesc(item: any) {
    let ret = item.object_type
    if (item.object_name) ret += ' ' + item.object_name
    if (item.object_internal_id) ret += ' #' + item.object_internal_id

    return ret
  },
}
