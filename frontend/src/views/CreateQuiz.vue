<template>
  <div class="create-quiz">
    <div class="card-container">
      <h2 class="text-center text-white mb-4">📝 Create New Quiz</h2>

      <div class="mb-3">
        <label class="form-label text-white">Title:</label>
        <input
          v-model="title"
          type="text"
          class="form-control"
          placeholder="Enter quiz title"
        />
      </div>

      <div class="mb-3">
        <label class="form-label text-white">Description:</label>
        <textarea
          v-model="description"
          class="form-control"
          placeholder="Enter quiz description"
        ></textarea>
      </div>

      <div class="text-center">
        <button @click="submitQuiz" class="btn btn-success fw-bold">
          🚀 Create Quiz
        </button>
      </div>

      <div v-if="message" class="alert mt-3" :class="messageType">
        {{ message }}
      </div>

      <div class="text-center mt-4">
        <button @click="goBack" class="btn btn-secondary">
          🔙 Back to Dashboard
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateQuiz",
  data() {
    return {
      title: "",
      description: "",
      message: "",
      messageType: "",
    };
  },
  methods: {
    async submitQuiz() {
      if (!this.title.trim()) {
        this.message = "⚠️ Please fill in all required fields!";
        this.messageType = "alert-danger";
        return;
      }

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          "http://localhost:5000/api/admin/quizzes",
          {
            title: this.title,
            description: this.description,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        this.message = "✅ Quiz created successfully!";
        this.messageType = "alert-success";
        this.title = "";
        this.description = "";
      } catch (err) {
        console.error("Quiz creation failed:", err);
        this.message = "❌ Failed to create quiz!";
        this.messageType = "alert-danger";
      }
    },
    goBack() {
      this.$router.push("/admin-dashboard");
    },
  },
};
</script>

<style scoped>
.create-quiz {
  min-height: 100vh;
  background: linear-gradient(135deg, #8e2de2, #4a00e0);
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
  max-width: 700px;
}

.alert {
  text-align: center;
  font-weight: bold;
  padding: 10px;
}
.alert-success {
  background-color: #28a745;
  color: white;
}
.alert-danger {
  background-color: #dc3545;
  color: white;
}
</style>
