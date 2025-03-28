import { createRouter, createWebHistory } from "vue-router";
import SignupForm from "../views/SignupForm.vue";
import LoginForm from "../views/LoginForm.vue";
import UserDashboard from "../views/UserDashboard.vue";
import AdminDashboard from "../views/AdminDashboard.vue";

const routes = [
  {
    path: "/about",
    name: "About",
    component: () => import("@/views/LoginForm.vue"), // Or whatever component you have
  },

  { path: "/signup", component: SignupForm },
  { path: "/login", component: LoginForm },
  {
    path: "/dashboard",
    component: UserDashboard,
    meta: { requiresAuth: true, role: "user" },
  },
  { path: "/admin-dashboard", component: AdminDashboard },
  { path: "/", redirect: "/login" },
  {
    path: "/admin-dashboard/add-question",
    name: "AddQuestion",
    component: () => import("../views/AddQuestion.vue"),
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin-dashboard/manage-questions",
    name: "ManageQuestions",
    component: () => import("@/views/ManageQuestions.vue"),
  },
  {
    path: "/admin-dashboard/add-quiz",
    name: "CreateQuiz",
    component: () => import("../views/CreateQuiz.vue"),
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/play-quiz/:quizId",
    name: "PlayQuiz",
    component: () => import("../views/PlayQuiz.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Route Protection Middleware
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (to.path === "/dashboard" && (!token || role !== "user")) {
    next("/login");
  } else if (to.path === "/admin-dashboard" && (!token || role !== "admin")) {
    next("/login");
  } else {
    next();
  }
});
export default router;
