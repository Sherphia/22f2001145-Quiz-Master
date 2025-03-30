<template>
  <div class="mt-5">
    <h4 class="text-white text-center mb-3">📈 Your Score Trend</h4>
    <canvas ref="chartCanvas" height="150"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "UserPerformanceChart",
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chartInstance: null,
    };
  },
  mounted() {
    this.createChart();
  },
  watch: {
    results: {
      handler() {
        this.createChart();
      },
      deep: true,
    },
  },
  methods: {
    createChart() {
      const labels = this.results.map((r) => r.quiz_title);
      const scores = this.results.map((r) => r.percentage);

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const ctx = this.$refs.chartCanvas;
      this.chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Percentage Score",
              data: scores,
              fill: true,
              backgroundColor: "rgba(255, 255, 255, 0.2)",
              borderColor: "#fff",
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: "#fff",
              },
            },
          },
          scales: {
            x: {
              ticks: {
                color: "#fff",
              },
            },
            y: {
              beginAtZero: true,
              max: 100,
              ticks: {
                color: "#fff",
                stepSize: 10,
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
canvas {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 10px;
}
</style>
