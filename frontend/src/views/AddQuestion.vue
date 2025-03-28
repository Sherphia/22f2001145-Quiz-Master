<template>
  <div class="add-question-container">
    <div class="question-card">
      <h2 class="text-center mb-4 text-white">➕ Add New Question</h2>
      <!-- Back Button -->
      <div class="mb-3">
        <button
          class="btn btn-light fw-bold"
          @click="$router.push('/admin-dashboard')"
        >
          ⬅️ Back to Dashboard
        </button>
      </div>
      <!-- Quiz Selector -->
      <div class="mb-3">
        <label for="quiz" class="form-label text-white">Select Quiz</label>
        <select v-model="form.quiz_id" class="form-select" required>
          <option disabled value="">-- Choose a Quiz --</option>
          <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
            {{ quiz.title }}
          </option>
        </select>
      </div>
      <form @submit.prevent="submitQuestion">
        <!-- Question Text -->
        <div class="mb-3">
          <label class="form-label text-white">Question Text</label>
          <textarea
            class="form-control"
            v-model="form.question_text"
            required
          ></textarea>
        </div>

        <!-- Question Type -->
        <div class="mb-3">
          <label class="form-label text-white">Question Type</label>
          <select class="form-select" v-model="form.question_type" required>
            <option value="">Select Type</option>
            <option value="mcq">MCQ</option>
            <option value="msq">MSQ</option>
            <option value="numeric">Numeric</option>
            <option value="text">Text</option>
          </select>
        </div>

        <!-- Options for MCQ/MSQ -->
        <div
          v-if="form.question_type === 'mcq' || form.question_type === 'msq'"
        >
          <label class="form-label text-white">Options (min 2)</label>
          <div
            v-for="(opt, idx) in form.options"
            :key="idx"
            class="input-group mb-2"
          >
            <input
              class="form-control"
              v-model="form.options[idx]"
              placeholder="Option"
            />
            <button
              class="btn btn-danger"
              type="button"
              @click="removeOption(idx)"
              v-if="form.options.length > 2"
            >
              ❌
            </button>
          </div>
          <button class="btn add-option mb-3" type="button" @click="addOption">
            ➕ Add Option
          </button>
        </div>

        <!-- Correct Answer -->
        <div class="mb-3">
          <label class="form-label text-white">Correct Answer</label>

          <input
            v-if="form.question_type === 'mcq'"
            type="number"
            class="form-control"
            v-model.number="form.correct_answer"
            placeholder="Correct option index (e.g., 0 for first)"
            required
          />

          <div v-else-if="form.question_type === 'msq'">
            <label class="form-text text-light">
              Enter comma-separated option indices (e.g., 0,2)
            </label>
            <input
              type="text"
              class="form-control"
              v-model="form.correct_answer"
              placeholder="e.g., 0,2"
              required
            />
          </div>

          <input
            v-else
            type="text"
            class="form-control"
            v-model="form.correct_answer"
            placeholder="Correct answer"
            required
          />
        </div>

        <!-- Submit -->
        <div class="text-center mt-4">
          <button type="submit" class="btn btn-success fw-bold">
            Submit Question
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddQuestion",
  data() {
    return {
      form: {
        question_text: "",
        question_type: "",
        options: ["", ""],
        correct_answer: "",
        quiz_id: "",
      },
      quizzes: [],
    };
  },
  mounted() {
    this.fetchQuizzes();
  },
  methods: {
    async fetchQuizzes() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:5000/api/quizzes", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.quizzes = res.data.quizzes;
      } catch (err) {
        console.error("❌ Error fetching quizzes:", err);
        alert("Failed to load quizzes!");
      }
    },
    addOption() {
      this.form.options.push("");
    },
    removeOption(index) {
      this.form.options.splice(index, 1);
    },
    async submitQuestion() {
      let formattedAnswer = this.form.correct_answer;

      // Convert correct_answer based on question type
      if (this.form.question_type === "mcq") {
        formattedAnswer = parseInt(this.form.correct_answer);
      } else if (this.form.question_type === "msq") {
        formattedAnswer = this.form.correct_answer
          .split(",")
          .map((index) => parseInt(index.trim()));
      } else if (this.form.question_type === "numeric") {
        formattedAnswer = parseFloat(this.form.correct_answer);
      }

      const payload = {
        question_text: this.form.question_text,
        question_type: this.form.question_type,
        options:
          this.form.question_type === "mcq" || this.form.question_type === "msq"
            ? this.form.options
            : [],
        correct_answer: formattedAnswer,
        quiz_id: this.form.quiz_id,
      };

      console.log("Payload being sent:", JSON.stringify(payload, null, 2)); // Debug log

      try {
        await axios.post("http://localhost:5000/api/admin/questions", payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        alert("✅ Question added successfully!");
        // Reset form
        this.form = {
          question_text: "",
          question_type: "",
          options: ["", ""],
          correct_answer: "",
        };
      } catch (error) {
        console.error(
          "❌ Error submitting question:",
          error.response?.data || error.message
        );
        alert("❌ Error submitting question");
      }
    },
  },
};
</script>

<style scoped>
.add-question-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #2b5876, #4e4376);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.question-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem 3rem;
  border-radius: 20px;
  backdrop-filter: blur(12px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 700px;
}

.add-option {
  background: linear-gradient(135deg, #c6ccef, #b0b4c1);
  color: white;
  font-weight: bold;
  border: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.add-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(2, 10, 43, 0.5);
}
</style>
