<!-- frontend/src/App.vue -->
<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content p-3">
        <h1>Configuration Manager</h1>
        <div class="header-nav">
          <router-link to="/">Instruments</router-link>
        </div>
      </div>
    </header>
    
    <main class="app-content p-3">
      <Toast />
      <router-view />
    </main>
    
    <footer class="app-footer p-2">
      <div class="footer-content">
        <p>Configuration Manager © 2025</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Using Vue 3 Composition API
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #3b82f6;
  color: white;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.header-nav a {
  color: white;
  text-decoration: none;
  margin-left: 1rem;
}

.app-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: #f8f9fa;
  color: #6c757d;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  text-align: center;
}
</style>
