import { defineConfig, loadEnv } from 'vite';
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), 'VITE_');
  return { server: { host: '127.0.0.1', port: 5174, strictPort: true, proxy: { '/api': { target: env.VITE_BACKEND_TARGET || 'http://127.0.0.1:8002', rewrite: path => path.replace(/^\/api/, '') } } } };
});
