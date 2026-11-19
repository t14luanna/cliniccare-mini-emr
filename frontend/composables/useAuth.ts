import type { LoginResponse } from '~/types'

export function useAuth() {
  const token = useCookie<string | null>('token', { maxAge: 8 * 60 * 60, sameSite: 'strict' })
  const doctorName = useCookie<string | null>('doctor_name', { maxAge: 8 * 60 * 60, sameSite: 'strict' })

  const isLoggedIn = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const config = useRuntimeConfig()
    const response = await $fetch<LoginResponse>('/auth/login', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: { username, password },
    })
    token.value = response.access_token
    doctorName.value = response.doctor.full_name
  }

  function logout() {
    token.value = null
    doctorName.value = null
    return navigateTo('/login')
  }

  return { token, doctorName, isLoggedIn, login, logout }
}
