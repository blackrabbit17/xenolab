<script setup>
import ModelView from '@/views/ModelView.vue';
import LineChart from '@/components/graphs/LineChart.vue';
import Api from '@/lib/api';
import { ref, onMounted } from 'vue';

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

const lifeformData = ref(null);
const showFallbackImage = ref(false);
const videoElement = ref(null);

const handleVideoError = () => {
  console.error('Video stream failed to load');
  showFallbackImage.value = true;
};

const fetchLifeformData = async () => {
  try {
    const response = await Api.get('/lifeform/');
    lifeformData.value = response;
  } catch (error) {
    console.error('Error fetching lifeform data:', error);
  }
};

onMounted(async () => {
  await fetchLifeformData();
  
  // Attempt to reload video after a delay
  setTimeout(() => {
    if (videoElement.value) {
      videoElement.value.load();
    }
  }, 1000);
});
</script>
<template>
    <div class="top-container">
        <div class="left-container">
            <div class="left-container-content">
                <h1 v-if="lifeformData">LIFEFORM: <span class="lifeform-name">{{ lifeformData.lifeform }}</span></h1>
                <img src="http://192.168.88.31:8000/map/" alt="map" class="map-img">
            </div>
        </div>
        <div class="right-container">
            <img  
                src="http://192.168.88.31:8000/camera/stream/0/" 
                alt="Camera feed" 
                class="camera-feed"
                style="width: 100%; height: 100%; object-fit: contain;"
            >
        </div>
    </div>
    <div class="graph-container">
        <div class="graph-item-1">
            <h1 class="lower_graph_h1">Temperature</h1>
            <LineChart 
                :chart-data="temperatureData"
                :chart-options="chartOptions"
                :height="100"
                css-classes="chart-container"
                :styles="{ width: '100%' }"
            />
        </div>
        <div class="graph-item-2">
            <h1 class="lower_graph_h1">Humidity</h1>
            <LineChart 
                :chart-data="humidityData"
                :chart-options="chartOptions"
                :height="100"
                css-classes="chart-container"
                :styles="{ width: '100%' }"
            />
        </div>
        <div class="graph-item-3">
            <h1 class="lower_graph_h1">Soil Moisture</h1>
            <LineChart 
                :chart-data="soilMoistureData"
                :chart-options="chartOptions"
                :height="80"
                css-classes="chart-container"
                :styles="{ width: '100%' }"
            />
        </div>
        <div class="graph-item-4">
            <h1 class="lower_graph_h1">ATMOSPHERICS</h1>
            
            <div class="atmos-container">
                <div class="atmos-item">
                    Sunlight: ON
                    <img src="@/assets/light-on.png" alt="Light Off" class="control-icon">
                </div>
                <div class="atmos-item">
                    Wind: 0.4m/s
                    <img src="@/assets/wind-on.png" alt="Wind Off" class="control-icon">
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>
/* Add necessary container styling */
.right-container {
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.camera-feed {
    max-width: 100%;
    max-height: 100%;
}
</style>