<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav>
  <router-view />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 20px;
  background-color: #b8b6b6; /* soft pale yellow */
  border-bottom: 2px solid #727272;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

nav a {
  font-weight: bold;
  color: #4d4b4d; /* deep brownish-gold text for visibility */
  margin: 0 15px;
  text-decoration: none;
  transition: color 0.3s ease;
}

nav a:hover {
  color: #050505; /* warm gold on hover */
}

nav a.router-link-exact-active {
  color: #0e0d0d; /* strong yellow-orange for active state */
}
</style>
