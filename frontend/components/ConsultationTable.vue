<script setup lang="ts">
import type { Consultation } from '~/types'

defineProps<{
  consultations: Consultation[]
}>()

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}
</script>

<template>
  <p v-if="consultations.length === 0" class="muted">No consultations found.</p>

  <table v-else class="table">
    <thead>
      <tr>
        <th>Date</th>
        <th>Patient</th>
        <th>Diagnoses</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="consultation in consultations" :key="consultation.id">
        <td class="nowrap">{{ formatDate(consultation.created_at) }}</td>
        <td class="nowrap">{{ consultation.patient_name }}</td>
        <td>
          <span
            v-for="diagnosis in consultation.diagnoses"
            :key="diagnosis.code"
            class="tag"
            :title="diagnosis.description"
          >
            {{ diagnosis.code }}
          </span>
        </td>
        <td class="notes">{{ consultation.notes }}</td>
      </tr>
    </tbody>
  </table>
</template>
