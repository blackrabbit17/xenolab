<script setup>
</script>
<style scoped>
.top-container {
    position: relative;
    height: 300px;
}
.graph-container {
    position: relative;
    height: 160px;
    top: 10px;
    display: flex;
    margin-top: 20px;
}
.left-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 50%;
    height: 100%;
    background: rgba(30, 40, 50, 0.8);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px rgba(255, 255, 255, 0.1);
    transform: perspective(1000px) rotateX(2deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    backdrop-filter: blur(8px);
    padding: 15px;
}
.right-container {
    position: absolute;
    top: 0;
    right: 0;
    width: 50%;
    height: 100%;
    background: rgba(30, 40, 50, 0.8);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px rgba(255, 255, 255, 0.1);
    transform: perspective(1000px) rotateX(2deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    backdrop-filter: blur(8px);
    padding: 15px;
}
.left-container:hover, .right-container:hover {
    transform: perspective(1000px) rotateX(0deg);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2), inset 0 1px rgba(255, 255, 255, 0.15);
}
.graph-item-1, .graph-item-2, .graph-item-3, .graph-item-4 {
    position: absolute;
    width: 25%;
    height: 100%;
    background: rgba(40, 45, 55, 0.7);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12), inset 0 1px rgba(255, 255, 255, 0.08);
    transform: perspective(800px) rotateY(1deg);
    transition: all 0.3s ease;
    padding: 12px;
    backdrop-filter: blur(5px);
}
.graph-item-1:hover, .graph-item-2:hover, .graph-item-3:hover, .graph-item-4:hover {
    transform: perspective(800px) rotateY(0deg) translateZ(5px);
    box-shadow: 0 5px 12px rgba(0, 0, 0, 0.18), inset 0 1px rgba(255, 255, 255, 0.12);
    background: rgba(45, 50, 60, 0.8);
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
    font-size: 1.0rem;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #00e5ff, #2979ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 10px;
    font-weight: 700;
    position: relative;
    padding-bottom: 2px;
}

h1::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg, #00e5ff, transparent);
}

</style>
<template>
    <div class="top-container">
        <div class="left-container">
            <div class="left-container-content">
                <h1>Home</h1>
            </div>
        </div>
        <div class="right-container">
            <div class="right-container-content">
                <h1>Home</h1>
            </div>
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