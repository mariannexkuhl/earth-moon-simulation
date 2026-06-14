import * as THREE from './libs/three.module.js';
import { OrbitControls } from './libs/OrbitControls.js';

// Constants
const G = 6.67430e-11; // m³·kg⁻¹·s⁻²
const M_earth = 5.972e24; // kg
const M_moon = 7.348e22; // kg
const R_earth = 6.371e6; // m
const R_moon = 1.737e6; // m
const R_earth_moon = 3.844e8; // m
const dt = 3600; // s
const steps = 500;

// Precompute motion
let posEarth = new THREE.Vector3(0, 0, 0);
let posMoon = new THREE.Vector3(R_earth_moon, 0, 0);
let velEarth = new THREE.Vector3(0, 0, 0);
let velMoon = new THREE.Vector3(0, 1022, 0); // m/s

const earthPositions = [];
const moonPositions = [];

for (let i = 0; i < steps; i++) {
  const rVec = new THREE.Vector3().subVectors(posMoon, posEarth);
  const r = rVec.length();
  const F = (G * M_earth * M_moon) / (r * r);
  const aEarth = rVec.clone().multiplyScalar(F / (r * M_earth));
  const aMoon = rVec.clone().multiplyScalar(-F / (r * M_moon));

  velMoon.addScaledVector(aMoon, dt);
  velEarth.addScaledVector(aEarth, dt);
  posMoon.addScaledVector(velMoon, dt);
  posEarth.addScaledVector(velEarth, dt);

  earthPositions.push(posEarth.clone());
  moonPositions.push(posMoon.clone());
}

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1e6, 1e10);
camera.position.set(0, 0, 8e8);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);

// Earth
const earthGeometry = new THREE.SphereGeometry(R_earth * 100, 32, 32); // scale x100 for visibility
const earthMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
const earthMesh = new THREE.Mesh(earthGeometry, earthMaterial);
scene.add(earthMesh);

// Moon
const moonGeometry = new THREE.SphereGeometry(R_moon * 100, 32, 32);
const moonMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
const moonMesh = new THREE.Mesh(moonGeometry, moonMaterial);
scene.add(moonMesh);

// Light
const light = new THREE.PointLight(0xffffff, 1);
light.position.set(0, 0, 0);
scene.add(light);

// Animation
let frame = 0;
function animate() {
  requestAnimationFrame(animate);
  if (frame < steps) {
    const ep = earthPositions[frame];
    const mp = moonPositions[frame];
    earthMesh.position.set(ep.x, ep.y, ep.z);
    moonMesh.position.set(mp.x, mp.y, mp.z);
    frame++;
  }
  controls.update();
  renderer.render(scene, camera);
}
animate();
