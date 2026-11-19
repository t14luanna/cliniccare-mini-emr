<script setup lang="ts">
import type { Consultation } from '~/types'

const PAGE_SIZE = 10

const api = useApi()

const consultations = ref<Consultation[]>([])
const page = ref(1)
const loading = ref(true)
const error = ref('')

// no total count from the API, so a full page = maybe more
const hasNextPage = computed(() => consultations.value.length === PAGE_SIZE)

async function loadConsultations() {
  loading.value = true
  error.value = ''
  try {
    consultations.value = await api<Consultation[]>('/consultation', {
      query: { limit: PAGE_SIZE, offset: (page.value - 1) * PAGE_SIZE },
    })
  } catch (e) {
    error.value = getErrorMessage(e)
  } finally {
    loading.value = false
  }
}

function goToPage(newPage: number) {
  page.value = newPage
  loadConsultations()
}

onMounted(loadConsultations)
</script>

<template>
  <div>
    <div class="page-title">
      <h1>Consultations</h1>
      <NuxtLink to="/consultations/new" class="button">+ New consultation</NuxtLink>
    </div>

    <p v-if="loading" class="muted">Loading...</p>
    <p v-else-if="error" class="error">{{ error }}</p>
    <template v-else>
      <ConsultationTable :consultations="consultations" />
      <Pagination :page="page" :has-next-page="hasNextPage" @change="goToPage" />
    </template>
  </div>
</template>
