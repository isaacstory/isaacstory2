import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Base path: use VITE_BASE env var or default to '/'
// For Nginx: VITE_BASE=/isaacstory/ npm run build
// For GitHub Pages: npm run build (uses '/')
const base = process.env.VITE_BASE || '/'

export default defineConfig({
  plugins: [vue()],
  base,
  build: {
    outDir: 'dist',
    emptyOutDir: true
  }
})
