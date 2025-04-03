<script setup>
import ModelView from '@/views/ModelView.vue';
import LineChart from '@/components/graphs/LineChart.vue';

// Sample data for the graphs
const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const temperatureData = {
  labels: labels,
  datasets: [
    {
      label: 'Temperature (°C)',
      data: [22, 23, 24, 25, 26, 25, 24, 23, 22, 21, 20, 19],
      fill: true,
      borderColor: '#FF6B6B',
      backgroundColor: 'rgba(255, 107, 107, 0.2)',
      tension: 0.4
    }
  ]
};

const humidityData = {
  labels: labels,
  datasets: [
    {
      label: 'Humidity (%)',
      data: [45, 50, 55, 60, 65, 62, 58, 55, 50, 47, 45, 42],
      fill: true,
      borderColor: '#48DBFB',
      backgroundColor: 'rgba(72, 219, 251, 0.2)',
      tension: 0.4
    }
  ]
};

const soilMoistureData = {
  labels: labels,
  datasets: [
    {
      label: 'Soil Moisture (%)',
      data: [70, 65, 60, 55, 50, 45, 40, 38, 35, 33, 30, 28],
      fill: true,
      borderColor: '#1DD1A1',
      backgroundColor: 'rgba(29, 209, 161, 0.2)',
      tension: 0.4
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(20, 30, 40, 0.9)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: 'rgba(0, 229, 255, 0.3)',
      borderWidth: 1
    }
  },
  scales: {
    x: {
      display: false
    },
    y: {
      display: true,
      grid: {
        color: 'rgba(255, 255, 255, 0.05)',
        borderDash: [2, 4]
      },
      ticks: {
        color: 'rgba(255, 255, 255, 0.5)',
        font: {
          size: 9
        },
        padding: 10,
        maxTicksLimit: 5
      }
    }
  },
  elements: {
    point: {
      radius: 2,
      hoverRadius: 4,
      borderWidth: 2
    },
    line: {
      borderWidth: 2
    }
  },
  animation: {
    duration: 800,
    easing: 'easeOutQuart'
  }
};
</script>
<style scoped>
.top-container {
    position: relative;
    height: 300px;
}
.graph-container {
    position: relative;
    height: 160px;
    top: 0;
    display: flex;
    margin-top: 0;
}
.left-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 50%;
    height: 100%;
    background: rgba(30, 40, 50, 0.8);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px rgba(255, 255, 255, 0.1);
}
.right-container {
    position: absolute;
    top: 0;
    right: 0;
    width: 50%;
    height: 100%;
    background: rgba(30, 40, 50, 0.8);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px rgba(255, 255, 255, 0.1);
}
.graph-item-1, .graph-item-2, .graph-item-3, .graph-item-4 {
    position: absolute;
    width: 25%;
    height: 100%;
    background: rgba(40, 45, 55, 0.7);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12), inset 0 1px rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
}
.graph-item-1 {
    left: 0;
}
.graph-item-2 {
    left: 25%;
}
.graph-item-3 {
    left: 50%;
}
.graph-item-4 {
    left: 75%;
}

h1 {
    text-transform: uppercase;
    font-size: 0.95rem;
    letter-spacing: 1px;
    background: rgb(190, 190, 190);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    position: relative;
    padding: 6px;
}

h1::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg,rgba(0, 229, 255, 0.50), transparent);
}


.lower_graph_h1 {
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 1px;
    background: rgb(190, 190, 190);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    position: relative;
    padding: 3px;
}

.lower_graph_h1::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg,rgba(0, 229, 255, 0.50), transparent);
}

.left-container-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.model-view-container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.cam-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    padding-top: 36px;
}

.chart-container {
    flex: 1;
    overflow: hidden;
}
</style>
<template>
    <div class="top-container">
        <div class="left-container">
            <div class="left-container-content">
                <h1>Drosera binata</h1>
                <ModelView class="model-view-container" />
            </div>
        </div>
        <div class="right-container">
            <img class="cam-img" src="@/assets/test_camera.png" alt="cam-img">
        </div>
    </div>
    <div class="graph-container">
        <div class="graph-item-1">
            <h1 class="lower_graph_h1">Temperature</h1>
            <LineChart 
                :chart-data="temperatureData"
                :chart-options="chartOptions"
                :height="110"
                css-classes="chart-container"
                :styles="{ width: '100%' }"
            />
        </div>
        <div class="graph-item-2">
            <h1 class="lower_graph_h1">Humidity</h1>
            <LineChart 
                :chart-data="humidityData"
                :chart-options="chartOptions"
                :height="110"
                css-classes="chart-container"
                :styles="{ width: '100%' }"
            />
        </div>
        <div class="graph-item-3">
            <h1 class="lower_graph_h1">Soil Moisture</h1>
            <LineChart 
                :chart-data="soilMoistureData"
                :chart-options="chartOptions"
                :height="110"
                css-classes="chart-container"
                :styles="{ width: '100%' }"
            />
        </div>
        <div class="graph-item-4">
            <h1 class="lower_graph_h1">Artificial</h1>
            <div>Light</div>
            <div>Wind</div>
        </div>
    </div>

</template>