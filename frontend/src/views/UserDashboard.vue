<template>
  <div class="dashboard-container">
    <div class="card glassy-card" v-if="user">
      <h2 class="text-center mb-4 text-glow">🎉 Welcome to Quiz Master! 🧩</h2>
      <p class="text-center">
        Hello, <strong>{{ user.full_name }}</strong
        >!
      </p>
      <p class="text-center">📧 Email: {{ user.email }}</p>
      <p class="text-center">🎓 Qualification: {{ user.qualification }}</p>
      <p class="text-center">🎂 Date of Birth: {{ user.dob }}</p>

      <div class="text-center mt-4">
        <button
          @click="logout"
          class="btn btn-danger fw-bold px-4 py-2 glow-button"
        >
          Logout
        </button>
      </div>
    </div>

    <div class="card glassy-card mt-5 w-100" v-if="quizzes.length">
      <h3 class="text-center mb-4 text-glow">🧠 Available Quizzes</h3>

      <div class="mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="🔍 Search quiz by title..."
          v-model="searchQuery"
        />
      </div>

      <div
        v-for="quiz in filteredQuizzes"
        :key="quiz.id"
        class="quiz-box p-3 my-3 rounded"
      >
        <h5 class="fw-bold text-glow">📘 {{ quiz.title }}</h5>
        <p class="mb-2">📝 {{ quiz.description }}</p>
        <button class="btn btn-primary glow-button" @click="playQuiz(quiz.id)">
          Play Quiz ▶️
        </button>
      </div>
      <div class="text-center mt-4">
        <h5 class="text-white mb-3">
          🚀 Track Your Progress & Download Insights
        </h5>
        <router-link
          to="/history"
          class="btn btn-outline-info glow-button me-2"
        >
          📊 View Quiz History
        </router-link>
        <button @click="downloadPDF" class="btn btn-success glow-button me-2">
          📄 Download PDF
        </button>
        <button
          @click="downloadCSV"
          class="btn btn-warning glow-button text-dark"
        >
          🧾 Download CSV
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserDashboard",
  data() {
    return {
      user: null,
      quizzes: [],
      searchQuery: "",
    };
  },
  computed: {
    filteredQuizzes() {
      const q = this.searchQuery.toLowerCase();
      return this.quizzes.filter((quiz) =>
        quiz.title.toLowerCase().includes(q)
      );
    },
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      if (!token) return this.$router.push("/login");

      const userRes = await axios.get("http://localhost:5000/api/user", {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.user = userRes.data.user;

      const quizRes = await axios.get("http://localhost:5000/api/quizzes", {
        headers: { Authorization: `Bearer ${token}` },
      });
      this.quizzes = quizRes.data.quizzes;
    } catch (err) {
      alert("Session expired. Please login again.");
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    },
    playQuiz(quizId) {
      this.$router.push(`/play-quiz/${quizId}`);
    },
    downloadPDF() {
      const token = localStorage.getItem("token");
      axios
        .get("http://localhost:5000/api/user/pdf-report", {
          headers: { Authorization: `Bearer ${token}` },
          responseType: "blob", // Important for files
        })
        .then((res) => {
          const url = window.URL.createObjectURL(new Blob([res.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "quiz_report.pdf");
          document.body.appendChild(link);
          link.click();
        })
        .catch(() => {
          alert("Failed to download PDF report.");
        });
    },

    downloadCSV() {
      const token = localStorage.getItem("token");
      axios
        .get("http://localhost:5000/api/user/csv-report", {
          headers: { Authorization: `Bearer ${token}` },
          responseType: "blob", // For CSV too
        })
        .then((res) => {
          const url = window.URL.createObjectURL(new Blob([res.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "quiz_report.csv");
          document.body.appendChild(link);
          link.click();
        })
        .catch(() => {
          alert("Failed to download CSV report.");
        });
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(to right, #2b5876, #4e4376); /* Purple Gradient */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.glassy-card {
  background: rgba(0, 0, 0, 0.4);
  border-radius: 20px;
  padding: 3rem;
  backdrop-filter: blur(16px);
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
  width: 100%;
  max-width: 800px;
  color: #d4f1f9;
  font-size: 1.1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.text-glow {
  color: #a7f0f9;
  text-shadow: 0 0 1px #a7f0f9, 0 0 15px #88e0ef, 0 0 30px #58d5e7;
}

.glow-button {
  background-color: #00f7ff;
  color: #000;
  border: none;
  font-weight: bold;
  box-shadow: 0 0 12px rgba(0, 247, 255, 0.7);
  transition: all 0.3s ease;
}
.glow-button:hover {
  color: rgb(12, 12, 12);
  box-shadow: 0 0 25px rgba(0, 247, 255, 1);
  transform: scale(1.05);
  background-color: #00e0ff;
}

.quiz-box {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e2f1ff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.quiz-box:hover {
  transform: scale(1.02);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
}

input.form-control {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
}
input.form-control::placeholder {
  color: #c7dfff;
}
</style>
