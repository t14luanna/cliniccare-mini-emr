<template>
  <div>
    <header class="header">
      <NuxtLink to="/" class="brand">ClinicCare</NuxtLink>
      <nav class="nav">
        <NuxtLink to="/">Consultations</NuxtLink>
        <NuxtLink to="/consultations/new">New consultation</NuxtLink>
        <NuxtLink to="/search">Search</NuxtLink>
      </nav>
    </header>

    <main class="container">
      <slot />
    </main>
  </div>
</template>
