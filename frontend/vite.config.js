// vite.config.js
export default {
    build: {
      rollupOptions: {
        external: ['treejs'] // Replace 'treejs' with the correct module name if different
      }
    }
  }