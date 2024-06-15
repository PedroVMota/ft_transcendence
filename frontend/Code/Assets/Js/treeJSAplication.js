// Importing Three.js
import * as THREE from 'three';

export function treeJSAplication() {
  // Create the scene
  const scene = new THREE.Scene();

  // Create a camera
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

  // Create a renderer and add it to the DOM
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);

  // Create a cube
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
  const cube = new THREE.Mesh(geometry, material);

  // Add the cube to the scene
  scene.add(cube);

  // Move the camera out so we can see the cube
  camera.position.z = 5;

  // The render loop
  function animate() {
    requestAnimationFrame(animate);

    // Rotate the cube
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    // Render the scene from the perspective of the camera
    renderer.render(scene, camera);
  }

  // Start the animation loop
  animate();
}