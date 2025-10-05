import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      'babf7188ce23.ngrok-free.app',
      '.ngrok-free.app',
      '.ngrok.io'
    ]
  }
})
