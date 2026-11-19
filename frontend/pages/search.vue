<script setup lang="ts">
import type { Consultation } from '~/types'

const PAGE_SIZE = 10

const api = useApi()

const patient = ref('')
const diagnosisCode = ref('')
const results = ref<Consultation[]>([])
const page = ref(1)
const searched = ref(false)
const loading = ref(false)
const error = ref('')

const hasNextPage = computed(() => results.value.length === PAGE_SIZE)

async function loadResults() {
  loading.value = true
  error.value = ''
  try {
    const query: Record<string, string | number> = {
      limit: PAGE_SIZE,
      offset: (page.value - 1) * PAGE_SIZE,
    }
    if (patient.value.trim()) query.patient = patient.value.trim()
    if (diagnosisCode.value.trim()) query.diagnosis_code = diagnosisCode.value.trim()

    results.value = await api<Consultation[]>('/consultation', { query })
    searched.value = true
  } catch (e) {
    error.value = getErrorMessage(e)
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  loadResults()
}

function goToPage(newPage: number) {
  page.value = newPage
  loadResults()
}

function clear() {
  patient.value = ''
  diagnosisCode.value = ''
  results.value = []
  page.value = 1
  searched.value = false
}
</script>

<template>
  <div>
    <h1>Search consultations</h1>

    <form class="card search-form" @submit.prevent="search">
      <div class="field">
        <label for="patient">Patient name</label>
        <input id="patient" v-model="patient" placeholder="e.g. Nguyen" />
      </div>
      <div class="field">
        <label for="code">Diagnosis code</label>
        <input id="code" v-model="diagnosisCode" placeholder="e.g. E11.9" />
      </div>
      <div class="actions">
        <button class="button" type="submit" :disabled="loading">Search</button>
        <button class="button secondary" type="button" @click="clear">Clear</button>
      </div>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-else-if="loading" class="muted">Searching...</p>
    <template v-else-if="searched">
      <ConsultationTable :consultations="results" />
      <Pagination :page="page" :has-next-page="hasNextPage" @change="goToPage" />
    </template>
  </div>
</template>

<style scoped>
.search-form { display: flex; gap: 16px; align-items: flex-end; flex-wrap: wrap; }
.search-form .field { flex: 1; min-width: 200px; margin-bottom: 0; }
.actions { display: flex; gap: 8px; }
</style>
