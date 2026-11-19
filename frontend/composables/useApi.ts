export function useApi() {
  const config = useRuntimeConfig()
  const { token, logout } = useAuth()

  return $fetch.create({
    baseURL: config.public.apiBase,

    onRequest({ options }) {
      if (token.value) {
        options.headers.set('Authorization', `Bearer ${token.value}`)
      }
    },

    onResponseError({ response }) {
      if (response.status === 401) {
        logout()
      }
    },
  })
}

// FastAPI puts the error in `detail` (a list for 422)
export function getErrorMessage(error: any): string {
  const detail = error?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join(', ')
  return 'Something went wrong. Please try again.'
}
