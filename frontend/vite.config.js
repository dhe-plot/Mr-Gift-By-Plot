import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          clerk: ['@clerk/clerk-react'],
          stripe: ['@stripe/stripe-js', '@stripe/react-stripe-js'],
          router: ['react-router-dom'],
          ui: ['lucide-react', 'framer-motion', '@radix-ui/react-slot']
        }
      }
    },
    chunkSizeWarningLimit: 600
  },
  define: {
    global: 'globalThis',
  }
})
