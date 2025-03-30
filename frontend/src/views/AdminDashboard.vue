<template>
  <div class="admin-dashboard">
    <div class="card-container">
      <h2 class="text-center mb-4 text-white">👑 Admin Dashboard</h2>

      <!-- User Table -->
      <p class="text-white text-center fw-bold mb-4">
        List of Registered Users:
      </p>

      <div v-if="loading" class="text-white text-center mb-3">
        Loading users...
      </div>
      <div v-else>
        <table class="table table-hover table-bordered bg-white rounded shadow">
          <thead class="table-warning text-center">
            <tr>
              <th>#</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>DOB</th>
              <th>Qualification</th>
            </tr>
          </thead>
          <tbody class="text-center">
            <tr v-for="(user, index) in users" :key="user.id">
              <td>{{ index + 1 }}</td>
              <td>{{ user.full_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.dob }}</td>
              <td>{{ user.qualification }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="text-center mt-5">
        <button
          @click="$router.push('/admin-dashboard/add-quiz')"
          class="btn btn-light fw-bold"
        >
          ➕ Add Quiz
        </button>
      </div>

      <!-- Go to Add Question Page -->
      <div class="text-center mt-4">
        <button
          @click="$router.push('/admin-dashboard/add-question')"
          class="btn btn-light fw-bold"
        >
          ➕ Add Question
        </button>
      </div>

      <div class="text-center mt-4">
        <button
          @click="$router.push('/admin-dashboard/manage-questions')"
          class="btn btn-light fw-bold"
        >
          📋 Manage Questions
        </button>
      </div>
      <!-- Download Monthly Report -->
      <div class="text-center mt-4">
        <button @click="downloadMonthlyReport" class="btn btn-success fw-bold">
          📥 Download Monthly Report (CSV)
        </button>
      </div>
      <!-- Logout -->
      <div class="text-center mt-4">
        <button @click="logout" class="btn btn-danger fw-bold">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminDashboard",
  data() {
    return {
      users: [],
      loading: true,
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");

      if (!token || role !== "admin") {
        alert("Access denied!");
        return this.$router.push("/login");
      }

      const res = await axios.get("http://localhost:5000/api/admin/users", {
        headers: { Authorization: `Bearer ${token}` },
      });

      this.users = res.data.users;
    } catch (err) {
      console.error("Error fetching users:", err);
      alert("Failed to load users.");
    } finally {
      this.loading = false;
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    },
    async downloadMonthlyReport() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          "http://localhost:5000/api/admin/monthly-report",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const error = await response.json();
          alert("Error: " + (error.message || "Unable to download report"));
          return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "monthly_report.csv");
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error("Download error:", error);
        alert("Something went wrong while downloading the report.");
      }
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #3f0463, #372b3f);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.card-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem 3rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 900px;
}
</style>
