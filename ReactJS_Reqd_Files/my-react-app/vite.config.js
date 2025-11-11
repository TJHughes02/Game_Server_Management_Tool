import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') }
  },
   server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
        cookieDomainRewrite: 'localhost',
        // rewrite Set-Cookie so the browser sends the cookie back from :5173
        configure: (proxy /*, options*/) => {
          proxy.on('proxyRes', (proxyRes) => {
            const setCookie = proxyRes.headers['set-cookie']
            if (setCookie) {
              proxyRes.headers['set-cookie'] = setCookie.map((c) =>
                c
                  .replace(/; *Secure/gi, '')           // dev is http
                  .replace(/SameSite=None/gi, 'SameSite=Lax')
              )
            }
          })
        }
      }
    }
  }
})

// UPDATED TO FIX SESSIONS 11.11.25