import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import en from './locales/en.json'
import pl from './locales/pl.json'
import resizable from './directives/resizable'
import './style.css'

const savedLocale = localStorage.getItem('nemo_locale') || 'pl'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { en, pl },
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(i18n)
app.directive('resizable', resizable)
app.mount('#app')
