<script setup lang="ts">
definePageMeta({ layout: false })

const { login } = useAuth()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await login(username.value, password.value)
    await navigateTo('/')
  } catch (e) {
    error.value = getErrorMessage(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <form class="card login-card" @submit.prevent="submit">
      <h1>ClinicCare</h1>
      <p class="muted">Sign in to manage consultation notes</p>

      <div class="field">
        <label for="username">Username</label>
        <input id="username" v-model="username" autocomplete="username" required />
      </div>
      <div class="field">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" autocomplete="current-password" required />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button class="button" type="submit" :disabled="loading" style="width: 100%">
        {{ loading ? 'Signing in...' : 'Sign in' }}
      </button>
      <p class="muted hint">Demo account: doctor / doctor123</p>
    </form>
  </div>
</template>

<style scoped>
.login-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; }
.login-card { width: 100%; max-width: 360px; }
.login-card h1 { margin-top: 0; color: #0f766e; }
.hint { font-size: 13px; text-align: center; margin-bottom: 0; }
</style>
