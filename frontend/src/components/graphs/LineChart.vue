<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

export default {
  name: 'LineChart',
  components: { Line },
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      default: () => ({})
    },
    chartId: {
      type: String,
      default: 'line-chart'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 130
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => ({})
    },
    plugins: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    mergedOptions() {
      return {
        ...this.chartOptions,
        responsive: true,
        maintainAspectRatio: false
      }
    }
  }
}
</script>

<template>
  <div class="chart-wrapper">
    <Line
      :data="chartData"
      :options="mergedOptions"
      :chart-id="chartId"
      :width="width"
      :height="height"
      :css-classes="cssClasses"
      :styles="styles"
      :plugins="plugins"
    />
  </div>
</template>

<style scoped>
.chart-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}
</style> 