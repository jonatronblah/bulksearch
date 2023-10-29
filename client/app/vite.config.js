import { defineConfig } from 'vite'
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  server: {    // <-- this object is added
    port: 9000,
    host: true,
    hmr: {
      clientPort: 80,
    },
    watch: {
      usePolling: true
    }
  },
  plugins: [react()]
})