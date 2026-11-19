export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: false },

  // everything is behind login, no need for SSR
  ssr: false,

  css: ['~/assets/css/main.css'],

  app: {
    head: { title: 'ClinicCare' },
  },

  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
    },
  },
})
