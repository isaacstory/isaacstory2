<template>
  <div class="container">
    <header>
      <h1>🩺 Isaac Story</h1>
      <p class="subtitle">Documentação clínica organizada</p>
    </header>
    
    <main>
      <div class="card">
        <h2>👋 Bem-vindo!</h2>
        <p>
          Este site vai apresentar a documentação clínica do Isaac de forma 
          organizada e fácil de navegar.
        </p>
        <p class="status">
          <span class="badge">Em construção</span>
        </p>
      </div>
      
      <div class="features">
        <div class="feature">
          <span class="icon">📋</span>
          <h3>Consultas</h3>
          <p>Histórico de consultas médicas</p>
        </div>
        <div class="feature">
          <span class="icon">🔬</span>
          <h3>Exames</h3>
          <p>Resultados e laudos</p>
        </div>
        <div class="feature">
          <span class="icon">💊</span>
          <h3>Prescrições</h3>
          <p>Medicamentos e orientações</p>
        </div>
      </div>
    </main>
    
    <footer>
      <p>Isaac Story v0.1.0</p>
    </footer>
  </div>
</template>

<script setup>
// Future: import data from markdown/JSON files
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  opacity: 0.9;
  font-size: 1.1rem;
}

main {
  flex: 1;
}

.card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  margin-bottom: 2rem;
}

.card h2 {
  color: #333;
  margin-bottom: 1rem;
}

.card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.status {
  text-align: center;
}

.badge {
  background: #667eea;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.feature {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.feature .icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.5rem;
}

.feature h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.feature p {
  color: #666;
  font-size: 0.875rem;
}

footer {
  text-align: center;
  color: rgba(255,255,255,0.7);
  margin-top: 2rem;
  padding: 1rem;
}
</style>
