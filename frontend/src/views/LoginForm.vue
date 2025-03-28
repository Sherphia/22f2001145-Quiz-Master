<template>
  <div class="login-page">
    <div class="card-container">
      <h2 class="text-center mb-4">Login</h2>

      <!-- Role Toggle -->
      <div class="d-flex justify-content-center mb-3">
        <label class="me-3">
          <input type="radio" value="user" v-model="form.role" /> User
        </label>
        <label>
          <input type="radio" value="admin" v-model="form.role" /> Admin
        </label>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label>Email</label>
          <input
            v-model="form.email"
            type="email"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label>Password</label>
          <input
            v-model="form.password"
            type="password"
            class="form-control"
            required
          />
        </div>

        <button type="submit" class="btn btn-success w-100 fw-bold">
          Login
        </button>

        <p class="mt-3 text-center">
          Don't have an account?
          <router-link to="/signup">Sign up here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm",
  data() {
    return {
      form: {
        email: "",
        password: "",
        role: "user", // UI toggle only
      },
    };
  },
  methods: {
    async handleLogin() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/login",
          this.form
        );

        const token = res.data.token;
        const role = res.data.user.role;

        if (!token || !role) {
          alert("Login failed: Missing token or role");
          return;
        }

        // Save to localStorage
        localStorage.setItem("token", token);
        localStorage.setItem("role", role);

        alert(res.data.message);
        console.log("Logged in as:", role);

        //admin password - admin123
        // Redirect based on role from backend
        if (role === "admin") {
          this.$router.push("/admin-dashboard");
        } else {
          this.$router.push("/dashboard");
        }
      } catch (err) {
        console.error("Login error:", err);
        alert("Login failed 😢");
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  background: linear-gradient(to right, #d299c2, #fef9d7);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-container {
  background: #fff3fc;
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
}
</style>
