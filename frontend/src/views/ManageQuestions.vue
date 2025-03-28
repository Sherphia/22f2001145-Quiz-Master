<template>
  <div class="manage-questions">
    <div class="card-container">
      <h2 class="text-center text-white mb-4">📋 Manage Questions</h2>
      <!-- Filters -->
      <div class="row mb-4 text-white">
        <div class="col-md-6 mb-2 mb-md-0">
          <input
            v-model="filters.searchText"
            class="form-control"
            placeholder="🔍 Search by question text..."
          />
        </div>
        <div class="col-md-6">
          <select v-model="filters.questionType" class="form-select">
            <option value="">All Types</option>
            <option value="mcq">MCQ</option>
            <option value="msq">MSQ</option>
            <option value="numeric">Numeric</option>
            <option value="text">Text</option>
          </select>
        </div>
      </div>

      <!-- 🔽 QUIZ FILTER DROPDOWN -->
      <div class="mb-4">
        <label class="form-label text-white">Filter by Quiz:</label>
        <select v-model="selectedQuizId" class="form-select">
          <option value="">All Quizzes</option>
          <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
            {{ quiz.title }}
          </option>
        </select>
      </div>

      <div v-if="loading" class="text-white text-center">Loading...</div>
      <div v-else>
        <table class="table table-bordered bg-white rounded shadow">
          <thead class="table-primary text-center">
            <tr>
              <th>#</th>
              <th>Question</th>
              <th>Type</th>
              <th>Options</th>
              <th>Correct Answer</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody class="text-center">
            <tr v-for="(q, index) in filteredQuestions" :key="q.id">
              <td>{{ index + 1 }}</td>
              <td>{{ q.question_text }}</td>
              <td>{{ q.question_type }}</td>
              <td>
                <ul v-if="q.options && q.options.length">
                  <li v-for="(opt, i) in q.options" :key="i">{{ opt }}</li>
                </ul>
                <span v-else>N/A</span>
              </td>
              <td>
                <span v-if="typeof q.correct_answer === 'number'">
                  {{ q.options[q.correct_answer] }}
                </span>
                <span v-else-if="Array.isArray(q.correct_answer)">
                  <ul>
                    <li v-for="idx in q.correct_answer" :key="idx">
                      {{ q.options[idx] }}
                    </li>
                  </ul>
                </span>
                <span v-else>{{ q.correct_answer }}</span>
              </td>
              <td>
                <button
                  class="btn btn-sm btn-warning me-2"
                  @click="openEditModal(q)"
                >
                  Edit
                </button>
                <button
                  class="btn btn-sm btn-danger"
                  @click="deleteQuestion(q.id)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="text-center mt-4">
        <button @click="goBack" class="btn btn-secondary">
          🔙 Back to Dashboard
        </button>
      </div>

      <!-- Edit Modal -->
      <div
        class="modal fade"
        id="editModal"
        tabindex="-1"
        aria-labelledby="editModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header bg-primary text-white">
              <h5 class="modal-title" id="editModalLabel">✏️ Edit Question</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Question Text:</label>
                <input v-model="editForm.question_text" class="form-control" />
              </div>

              <div class="mb-3">
                <label class="form-label">Question Type:</label>
                <select v-model="editForm.question_type" class="form-select">
                  <option value="mcq">MCQ</option>
                  <option value="msq">MSQ</option>
                  <option value="numeric">Numeric</option>
                  <option value="text">Text</option>
                </select>
              </div>

              <div
                v-if="
                  editForm.question_type === 'mcq' ||
                  editForm.question_type === 'msq'
                "
                class="mb-3"
              >
                <label class="form-label">Options:</label>
                <div
                  v-for="(opt, i) in editForm.options"
                  :key="i"
                  class="input-group mb-2"
                >
                  <input v-model="editForm.options[i]" class="form-control" />
                  <button
                    class="btn btn-danger"
                    @click="removeOption(i)"
                    v-if="editForm.options.length > 2"
                  >
                    ❌
                  </button>
                </div>
                <button class="btn btn-secondary" @click="addOption">
                  ➕ Add Option
                </button>
              </div>

              <div class="mb-3" v-if="editForm.question_type === 'mcq'">
                <label class="form-label">Correct Answer:</label>
                <select v-model="editForm.correct_answer" class="form-select">
                  <option
                    v-for="(opt, i) in editForm.options"
                    :key="i"
                    :value="i"
                  >
                    {{ opt }}
                  </option>
                </select>
              </div>

              <div class="mb-3" v-if="editForm.question_type === 'msq'">
                <label class="form-label">Correct Answers:</label>
                <div
                  v-for="(opt, i) in editForm.options"
                  :key="i"
                  class="form-check"
                >
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :value="i"
                    v-model="editForm.correct_answer"
                  />
                  <label class="form-check-label">{{ opt }}</label>
                </div>
              </div>

              <div
                v-if="
                  editForm.question_type === 'numeric' ||
                  editForm.question_type === 'text'
                "
                class="mb-3"
              >
                <label class="form-label">Correct Answer:</label>
                <input v-model="editForm.correct_answer" class="form-control" />
              </div>
            </div>

            <div class="modal-footer">
              <button class="btn btn-secondary" data-bs-dismiss="modal">
                Close
              </button>
              <button class="btn btn-success" @click="updateQuestion">
                💾 Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";

export default {
  name: "ManageQuestions",
  data() {
    return {
      questions: [],
      quizzes: [], // 🔽 All quizzes
      selectedQuizId: "", // 🔽 Currently selected quiz filter
      loading: true,
      editForm: {
        id: null,
        question_text: "",
        question_type: "mcq",
        options: ["", ""],
        correct_answer: 0,
      },
      filters: {
        searchText: "",
        questionType: "",
      },
      modalInstance: null,
    };
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter((q) => {
        const matchesText = q.question_text
          .toLowerCase()
          .includes(this.filters.searchText.toLowerCase());

        const matchesType =
          !this.filters.questionType ||
          q.question_type === this.filters.questionType;

        const matchesQuiz =
          !this.selectedQuizId || q.quiz_id === parseInt(this.selectedQuizId);

        return matchesText && matchesType && matchesQuiz;
      });
    },
  },
  async mounted() {
    this.fetchQuestions();
    this.fetchQuizzes(); // 🔽 Get quizzes too
    this.modalInstance = new Modal(document.getElementById("editModal"), {
      backdrop: false,
    });
  },
  methods: {
    async fetchQuestions() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get(
          "http://localhost:5000/api/admin/questions",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.questions = res.data.questions;
      } catch (err) {
        console.error("Error fetching questions:", err);
        alert("Failed to load questions!");
      } finally {
        this.loading = false;
      }
    },
    async fetchQuizzes() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:5000/api/quizzes", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.quizzes = res.data.quizzes;
      } catch (err) {
        console.error("Error fetching quizzes:", err);
        alert("Failed to load quizzes!");
      }
    },
    goBack() {
      this.$router.push("/admin-dashboard");
    },
    async deleteQuestion(id) {
      if (!confirm("Are you sure you want to delete this question?")) return;
      try {
        const token = localStorage.getItem("token");
        await axios.delete(`http://localhost:5000/api/admin/questions/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.questions = this.questions.filter((q) => q.id !== id);
      } catch (err) {
        console.error("Failed to delete question:", err);
        alert("❌ Could not delete question.");
      }
    },
    openEditModal(question) {
      this.editForm = JSON.parse(JSON.stringify(question));
      if (
        this.editForm.question_type === "msq" &&
        !Array.isArray(this.editForm.correct_answer)
      ) {
        this.editForm.correct_answer = [];
      }
      this.modalInstance.show();
    },
    addOption() {
      this.editForm.options.push("");
    },
    removeOption(i) {
      if (this.editForm.options.length > 2) {
        this.editForm.options.splice(i, 1);
        if (
          this.editForm.question_type === "mcq" &&
          this.editForm.correct_answer >= this.editForm.options.length
        ) {
          this.editForm.correct_answer = 0;
        }
        if (this.editForm.question_type === "msq") {
          this.editForm.correct_answer = this.editForm.correct_answer.filter(
            (idx) => idx < this.editForm.options.length
          );
        }
      }
    },
    async updateQuestion() {
      try {
        const token = localStorage.getItem("token");
        const payload = { ...this.editForm };
        await axios.put(
          `http://localhost:5000/api/admin/questions/${payload.id}`,
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        await this.fetchQuestions();
        this.modalInstance.hide();
      } catch (err) {
        console.error("Error updating question:", err);
        alert("❌ Failed to update question.");
      }
    },
    computed: {
      filteredQuestions() {
        return this.questions.filter((q) => {
          const matchesText = q.question_text
            .toLowerCase()
            .includes(this.filters.searchText.toLowerCase());

          const matchesType =
            !this.filters.questionType ||
            q.question_type === this.filters.questionType;

          return matchesText && matchesType;
        });
      },
    },
  },
};
</script>

<style scoped>
.manage-questions {
  background: linear-gradient(135deg, #00c6ff, #0072ff);
  min-height: 100vh;
  padding: 50px 20px;
}

.card-container {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  border-radius: 15px;
  padding: 30px;
  max-width: 1200px;
  margin: auto;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

::v-deep .modal-content {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  border-radius: 15px;
  border: none;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

::v-deep .modal-dialog {
  max-width: 800px;
  margin: auto;
  pointer-events: auto;
  z-index: 9999;
}

::v-deep .modal-header {
  border-bottom: none;
}

::v-deep .modal-footer {
  border-top: none;
}

::v-deep .modal {
  background: transparent !important;
}

.form-label {
  font-weight: bold;
  font-size: 1.1rem;
}
</style>
