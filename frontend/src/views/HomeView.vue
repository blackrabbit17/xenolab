<script setup>
import ModelView from '@/views/ModelView.vue';

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
    padding: 6px;
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
    width: 70%;
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
        <div class="graph-item-1">Temperature</div>
        <div class="graph-item-2">Humidity</div>
        <div class="graph-item-3">Soil Moisture</div>
        <div class="graph-item-4">
            Artificial
            <div>Light</div>
            <div>Wind</div>
        </div>
    </div>

</template>