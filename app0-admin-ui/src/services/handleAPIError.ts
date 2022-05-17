// function to handle properly hopeit api errors and throw a simplified error to UI
export const handleAPIError = (error: any) => {
  console.log('handle api error')
  let message
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    console.log(error.response.status)
    console.log(error.response.data)
    message = 'ERROR ' + error.response.status
    if (error.response.data.msg) {
      message += ': ' + error.response.data.msg
    } else if (typeof error.response.data === 'string') {
      message += ': ' + error.response.data
    } else if (typeof error.response.data === 'object') {
      message += ': ' + Object.values(error.response.data)
    } else {
      console.log(typeof error.response.data)
      message += ': ' + error.response.data
    }
  } else if (error.request) {
    // The request was made but no response was received
    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
    // http.ClientRequest in node.js
    console.log(error.request)
    message = 'ERROR: no response was received'
  } else {
    // Something happened in setting up the request that triggered an Error
    console.log('Error', error.message)
    message = 'ERROR: something went wrong. ' + error.message
  }
  console.log(error)

  throw new Error(message)
}
