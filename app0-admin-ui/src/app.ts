import { createApp as createClientApp } from 'vue'

import { createHead } from '@vueuse/head'
import { createPinia } from 'pinia'
import { createRouter } from './router'
import TheApp from './TheApp.vue'
import './styles'

const plugins = import.meta.glob('./plugins/*.ts')

export type TheAppContext = Awaited<ReturnType<typeof createApp>>
export type ThePlugin = (theApp: TheAppContext) => void | Promise<void>

// this is a helper function to define plugins with autocompletion
export function definePlugin(plugin: ThePlugin) {
  return plugin
}

export async function createApp() {
  const app = createClientApp(TheApp)
  const router = createRouter()

  const head = createHead()
  app.use(head)

  const pinia = createPinia()
  app.use(pinia)

  const theApp = {
    app,
    router,
    head,
    pinia,
  }

  app.provide('theApp', theApp)

  for (const path in plugins) {
    try {
      const { default: plugin } = await plugins[path]()
      await plugin(theApp)
    } catch (error) {
      console.error(`Error while loading plugin "${path}".`)
      console.error(error)
    }
  }

  // use router after plugin registration, so we can register navigation guards
  app.use(theApp.router)

  return theApp
}
