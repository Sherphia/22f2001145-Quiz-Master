<template>
  <div
    class="quiz-container"
    v-if="quiz && Array.isArray(questions) && questions.length > 0"
  >
    <h2 class="text-center text-glow mb-4">{{ quiz.title }}</h2>
    <p class="text-center lead">{{ quiz.description }}</p>

    <!-- Show questions one by one -->
    <div class="question-card glassy-card" v-if="questions[currentQuestion]">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="badge bg-info text-dark px-3 py-2 shadow-sm">
          Question Type:
          {{ questions[currentQuestion].question_type.toUpperCase() }}
        </span>
        <span class="text-muted"
          >Q {{ currentQuestion + 1 }} / {{ questions.length }}</span
        >
      </div>

      <h3 class="question-text mb-4">
        {{ questions[currentQuestion].question_text }}
      </h3>

      <!-- MCQ: Radio Buttons -->
      <div
        v-if="questions[currentQuestion].question_type.toLowerCase() === 'mcq'"
      >
        <div
          v-for="(option, index) in questions[currentQuestion].options"
          :key="index"
          class="option-item border rounded p-2 mb-2"
          :class="{ 'bg-light': answers[currentQuestion] === option }"
        >
          <label class="w-100">
            <input
              type="radio"
              :name="'mcq_' + currentQuestion"
              :value="option"
              v-model="answers[currentQuestion]"
              class="form-check-input me-2"
            />
            {{ option }}
          </label>
        </div>
      </div>

      <!-- MSQ: Checkboxes -->
      <div v-else-if="questions[currentQuestion].question_type === 'msq'">
        <div
          v-for="(option, index) in questions[currentQuestion].options"
          :key="index"
          class="option-item border rounded p-2 mb-2"
          :class="{ 'bg-light': answers[currentQuestion].includes(option) }"
        >
          <label class="w-100">
            <input
              type="checkbox"
              :value="option"
              :checked="answers[currentQuestion].includes(option)"
              @change="toggleMSQOption(option)"
              class="form-check-input me-2"
            />
            {{ option }}
          </label>
        </div>
      </div>

      <!-- Text/Numeric Input -->
      <div
        v-else-if="
          ['text', 'numeric'].includes(questions[currentQuestion].question_type)
        "
        class="mt-3"
      >
        <input
          type="text"
          v-model="answers[currentQuestion]"
          class="form-control"
          :placeholder="
            questions[currentQuestion].question_type === 'numeric'
              ? 'Enter a number'
              : 'Type your answer'
          "
        />
      </div>

      <!-- Navigation buttons -->
      <div class="navigation-buttons mt-4 d-flex justify-content-between">
        <button
          class="btn btn-secondary"
          @click="previousQuestion"
          :disabled="currentQuestion === 0"
        >
          Previous
        </button>
        <div>
          <button
            v-if="currentQuestion < questions.length - 1"
            class="btn btn-primary me-2"
            @click="nextQuestion"
          >
            Next
          </button>
          <button v-else class="btn btn-success" @click="submitQuiz">
            Submit Quiz
          </button>
        </div>
      </div>

      <!-- Quit Button -->
      <div class="text-center mt-3">
        <button class="btn btn-outline-danger" @click="confirmQuitQuiz">
          Quit Quiz
        </button>
      </div>
    </div>
  </div>

  <!-- Loading / Error States -->
  <div v-else-if="loading" class="text-center">Loading quiz...</div>
  <div v-else-if="error" class="text-center">
    {{ error }}
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PlayQuiz",
  data() {
    return {
      quiz: null,
      questions: [],
      currentQuestion: 0,
      answers: [],
      loading: false,
      error: null,
    };
  },
  async created() {
    this.fetchQuiz();
  },
  methods: {
    async fetchQuiz() {
      this.loading = true;
      const quizId = this.$route.params.quizId;
      console.log("👉 quizId from route:", quizId);
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          `http://localhost:5000/api/quizzes/${quizId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        this.quiz = response.data.quiz;
        this.questions = response.data.quiz.questions;
        this.answers = this.questions.map((q) =>
          ["MCQ", "MSQ"].includes(q.question_type.toUpperCase()) ? [] : ""
        );
      } catch (err) {
        console.error(
          "❌ Error fetching quiz:",
          err.response || err.message || err
        );
        this.error = "Failed to load quiz. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    isMultipleChoice(question) {
      return ["MCQ", "MSQ"].includes(question.question_type);
    },
    isSelectedOption(option) {
      return this.answers[this.currentQuestion].includes(option);
    },
    selectOption(option) {
      const currentAnswer = this.answers[this.currentQuestion];
      if (this.isMultipleChoice(this.questions[this.currentQuestion])) {
        if (currentAnswer.includes(option)) {
          // Unselect option
          this.answers[this.currentQuestion] = currentAnswer.filter(
            (opt) => opt !== option
          );
        } else {
          // Select option
          this.answers[this.currentQuestion].push(option);
        }
      } else {
        this.answers[this.currentQuestion] = [option];
      }
    },
    toggleMSQOption(option) {
      const currentAnswer = this.answers[this.currentQuestion];
      const index = currentAnswer.indexOf(option);
      if (index > -1) {
        currentAnswer.splice(index, 1); // Deselect
      } else {
        currentAnswer.push(option); // Select
      }
    },
    previousQuestion() {
      if (this.currentQuestion > 0) {
        this.currentQuestion--;
      }
    },
    nextQuestion() {
      if (this.currentQuestion < this.questions.length - 1) {
        this.currentQuestion++;
      }
    },
    async submitQuiz() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(
          "http://localhost:5000/api/submit-quiz",
          {
            quiz_id: this.quiz.id,
            answers: this.questions.map((q, index) => ({
              question_id: q.id,
              selected_answer: this.answers[index],
            })),
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        console.log("🔑 Token being sent:", token);
        // After submitting, navigate to results page or show result
        alert(`Your score: ${response.data.score}`);
        this.$router.push("/dashboard");
      } catch (err) {
        this.error = "Error submitting quiz. Please try again.";
      }
    },
    confirmQuitQuiz() {
      const confirmExit = confirm(
        "Are you sure you want to quit the quiz? Your progress will be lost."
      );
      if (confirmExit) {
        this.$router.push("/dashboard");
      }
    },
  },
};
</script>

<style scoped>
.quiz-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(to right, #d4fc79, #96e6a1);
  padding: 2rem;
}

.text-glow {
  text-shadow: 0 0 8px #fff, 0 0 15px #ff99bb, 0 0 30px #ff66a3;
}

.question-card {
  background: rgba(255, 255, 255, 0.2);
  padding: 2rem;
  border-radius: 20px;
  width: 100%;
  max-width: 700px;
  text-align: center;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
}

.option-item {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 12px;
  cursor: pointer;
}

.option-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.selected-option {
  background-color: #99ccff;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-weight: bold;
}

.quit-button-container {
  position: absolute;
  top: 20px;
  right: 30px;
}

.quit-button-container button {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 12px;
}
</style>
