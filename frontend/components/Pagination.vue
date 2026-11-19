<script setup lang="ts">
defineProps<{
  page: number
  hasNextPage: boolean
}>()

const emit = defineEmits<{
  change: [page: number]
}>()
</script>

<template>
  <div v-if="page > 1 || hasNextPage" class="pagination">
    <button class="button secondary" :disabled="page === 1" @click="emit('change', page - 1)">Previous</button>
    <span>Page {{ page }}</span>
    <button class="button secondary" :disabled="!hasNextPage" @click="emit('change', page + 1)">Next</button>
  </div>
</template>

<style scoped>
.pagination { display: flex; align-items: center; justify-content: flex-end; gap: 12px; margin-top: 16px; }
</style>
