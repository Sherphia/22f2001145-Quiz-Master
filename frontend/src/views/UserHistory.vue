<template>
  <div class="history-container">
    <div class="glass-card">
      <h2 class="text-center mb-4">📜 Your Quiz History</h2>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-light" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="results.length === 0" class="text-center text-white">
        You haven't taken any quizzes yet.
      </div>

      <div v-else>
        <table class="table table-hover table-bordered table-primary text-dark">
          <thead>
            <tr>
              <th>Date</th>
              <th>Quiz Title</th>
              <th>Score</th>
              <th>Total Marks</th>
              <th>Percentage</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(result, index) in results"
              :key="index"
              :class="getRowClass(result.percentage)"
            >
              <td>{{ result.date }}</td>
              <td>{{ result.quiz_title }}</td>
              <td>{{ result.score }}</td>
              <td>{{ result.total }}</td>
              <td>{{ result.percentage }}%</td>
            </tr>
          </tbody>
        </table>
        <!-- Chart showing score trend -->
        <UserPerformanceChart :results="results" />
      </div>

      <router-link to="/dashboard" class="btn btn-outline-light mt-4"
        >← Back to Dashboard</router-link
      >
    </div>
  </div>
</template>

<script>
import UserPerformanceChart from "./UserPerformanceChart.vue";
import axios from "axios";

export default {
  name: "UserHistory",
  components: {
    UserPerformanceChart,
  },
  data() {
    return {
      results: [],
      loading: true,
    };
  },
  mounted() {
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          "http://localhost:5000/api/user/results",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.results = response.data.results;
      } catch (error) {
        console.error("Error fetching quiz history:", error);
      } finally {
        this.loading = false;
      }
    },
    getRowClass(percentage) {
      if (percentage >= 80) return "table-success";
      else if (percentage >= 50) return "table-warning";
      else return "table-danger";
    },
  },
};
</script>

<style scoped>
.history-container {
  background: linear-gradient(to right, #667eea, #764ba2);
  min-height: 100vh;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(12px);
  padding: 30px;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
