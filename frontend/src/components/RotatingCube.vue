<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';

const containerRef = ref(null);
let scene, camera, renderer, cube;
let animationFrameId = null;

onMounted(() => {
  if (containerRef.value) {
    initThree();
    animate();
    
    // Force a resize after initialization
    setTimeout(() => {
      onWindowResize();
    }, 100);
  }
});

onBeforeUnmount(() => {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
  }
  if (renderer) {
    renderer.dispose();
  }
  window.removeEventListener('resize', onWindowResize);
});

function initThree() {
  // Create scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x1a1a1a);
  
  // Create camera
  camera = new THREE.PerspectiveCamera(
    75,
    containerRef.value.clientWidth / containerRef.value.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 5;
  
  // Create renderer
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(containerRef.value.clientWidth, containerRef.value.clientHeight);
  containerRef.value.appendChild(renderer.domElement);
  
  // Create cube
  const geometry = new THREE.BoxGeometry(2, 2, 2);
  const material = new THREE.MeshStandardMaterial({
    color: 0x00e5ff,
    metalness: 0.3,
    roughness: 0.4,
  });
  
  cube = new THREE.Mesh(geometry, material);
  scene.add(cube);
  
  // Add lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 5, 5);
  scene.add(directionalLight);

  // Handle window resize
  window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
  if (containerRef.value && camera && renderer) {
    camera.aspect = containerRef.value.clientWidth / containerRef.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(containerRef.value.clientWidth, containerRef.value.clientHeight);
  }
}

function animate() {
  animationFrameId = requestAnimationFrame(animate);
  
  // Very slow rotation
  if (cube) {
    cube.rotation.x += 0.002;
    cube.rotation.y += 0.001;
  }
  
  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
}
</script>

<template>
  <div class="cube-container" ref="containerRef"></div>
</template>

<style scoped>
.cube-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: block;
}
</style> 