<script setup lang="ts">
import type { Consultation, ConsultationCreate, Diagnosis } from '~/types'

const api = useApi()

const patientName = ref('')
const notes = ref('')
const diagnoses = ref<Diagnosis[]>([])
const saving = ref(false)
const error = ref('')

const canSubmit = computed(
  () => patientName.value.trim().length >= 2 && notes.value.trim() !== '' && diagnoses.value.length > 0,
)

async function submit() {
  error.value = ''
  saving.value = true
  try {
    const body: ConsultationCreate = {
      patient_name: patientName.value,
      notes: notes.value,
      diagnosis_codes: diagnoses.value.map((d) => d.code),
    }
    await api<Consultation>('/consultation', { method: 'POST', body })
    await navigateTo('/')
  } catch (e) {
    error.value = getErrorMessage(e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div>
    <h1>New consultation</h1>

    <form class="card" @submit.prevent="submit">
      <div class="field">
        <label for="patient">Patient name</label>
        <input id="patient" v-model="patientName" maxlength="100" placeholder="e.g. Nguyen Van A" />
      </div>

      <div class="field">
        <label>Diagnosis codes (ICD-10)</label>
        <DiagnosisPicker v-model="diagnoses" />
      </div>

      <div class="field">
        <label for="notes">Treatment notes</label>
        <textarea id="notes" v-model="notes" maxlength="5000" />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button class="button" type="submit" :disabled="!canSubmit || saving">
        {{ saving ? 'Saving...' : 'Save consultation' }}
      </button>
      <NuxtLink to="/" class="button secondary" style="margin-left: 8px">Cancel</NuxtLink>
    </form>
  </div>
</template>
