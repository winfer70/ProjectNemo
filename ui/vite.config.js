import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://nemo-api:8000',
      '/ws': { target: 'ws://nemo-api:8000', ws: true },
    },
  },
})
