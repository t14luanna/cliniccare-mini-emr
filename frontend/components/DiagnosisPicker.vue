<script setup lang="ts">
import type { Diagnosis } from '~/types'

const selected = defineModel<Diagnosis[]>({ required: true })

const api = useApi()
const search = ref('')
const results = ref<Diagnosis[]>([])
const error = ref('')

// wait until the user stops typing
let timer: ReturnType<typeof setTimeout> | undefined
watch(search, (term) => {
  clearTimeout(timer)
  if (!term.trim()) {
    results.value = []
    return
  }
  timer = setTimeout(async () => {
    error.value = ''
    try {
      results.value = await api<Diagnosis[]>('/diagnosis', { query: { search: term, limit: 10 } })
    } catch (e) {
      results.value = []
      error.value = getErrorMessage(e)
    }
  }, 300)
})

function isSelected(diagnosis: Diagnosis) {
  return selected.value.some((d) => d.code === diagnosis.code)
}

function add(diagnosis: Diagnosis) {
  if (!isSelected(diagnosis)) {
    selected.value = [...selected.value, diagnosis]
  }
  search.value = ''
}

function remove(code: string) {
  selected.value = selected.value.filter((d) => d.code !== code)
}
</script>

<template>
  <div>
    <div v-if="selected.length" class="selected">
      <span v-for="diagnosis in selected" :key="diagnosis.code" class="tag">
        {{ diagnosis.code }} – {{ diagnosis.description }}
        <button type="button" class="remove" @click="remove(diagnosis.code)">×</button>
      </span>
    </div>

    <input v-model="search" placeholder="Search by code or name, e.g. E11 or diabetes" />

    <p v-if="error" class="error">{{ error }}</p>

    <ul v-if="results.length" class="results">
      <li v-for="diagnosis in results" :key="diagnosis.code">
        <button type="button" :disabled="isSelected(diagnosis)" @click="add(diagnosis)">
          <strong>{{ diagnosis.code }}</strong> {{ diagnosis.description }}
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
input { width: 100%; }
.selected { margin-bottom: 8px; }
.remove { border: none; background: none; cursor: pointer; color: inherit; }
.results {
  list-style: none;
  margin: 4px 0 0;
  padding: 0;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
}
.results button {
  width: 100%;
  padding: 8px 10px;
  border: none;
  background: none;
  text-align: left;
  font: inherit;
  cursor: pointer;
}
.results button:hover:not(:disabled) { background: #f0fdfa; }
.results button:disabled { color: #9ca3af; cursor: default; }
</style>
