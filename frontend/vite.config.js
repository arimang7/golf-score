import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Vercel 배포 시 에셋 경로를 루트로 강제 (빈 화면 방지)
  base: '/',
  build: {
    outDir: 'dist',
    emptyOutDir: true
  }
})
