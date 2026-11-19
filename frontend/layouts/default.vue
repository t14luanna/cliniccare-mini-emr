<script setup lang="ts">
const { doctorName, logout } = useAuth()
</script>

<template>
  <div>
    <header class="header">
      <NuxtLink to="/" class="brand">ClinicCare</NuxtLink>
      <nav class="nav">
        <NuxtLink to="/">Consultations</NuxtLink>
        <NuxtLink to="/consultations/new">New consultation</NuxtLink>
        <NuxtLink to="/search">Search</NuxtLink>
      </nav>
      <span class="user">{{ doctorName }}</span>
      <button class="button secondary" @click="logout">Log out</button>
    </header>

    <main class="container">
      <slot />
    </main>
  </div>
</template>
