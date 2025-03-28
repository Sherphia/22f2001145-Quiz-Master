<template>
  <div class="signup-page">
    <div class="card-container">
      <h2 class="text-center mb-4">Create an Account</h2>
      <form @submit.prevent="handleSignup">
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
        <div class="mb-3">
          <label>Full Name</label>
          <input
            v-model="form.full_name"
            type="text"
            class="form-control"
            required
          />
        </div>
        <div class="mb-3">
          <label>Qualification</label>
          <input
            v-model="form.qualification"
            type="text"
            class="form-control"
            required
          />
        </div>
        <div class="mb-3">
          <label>Date of Birth</label>
          <input v-model="form.dob" type="date" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-warning w-100 fw-bold">
          Register
        </button>
        <p class="mt-3 text-center">
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignupForm",
  data() {
    return {
      form: {
        email: "",
        password: "",
        full_name: "",
        qualification: "",
        dob: "",
      },
    };
  },
  methods: {
    async handleSignup() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/signup",
          this.form
        );
        alert(res.data.message);
        this.$router.push("/login");
      } catch (err) {
        alert("Signup failed 😢");
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
.signup-page {
  background: linear-gradient(to right, #ffecd2, #fcb69f);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-container {
  background: #fff7e6;
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
}
</style>
