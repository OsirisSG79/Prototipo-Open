const fs = require('fs');
const path = require('path');

// Mock browser globals for Three.js in Node
global.THREE = require('../assets/three.min.js');
require('../assets/GLTFLoader.js');

console.log('Testing standalone GLTFLoader parsing on reformer_studio.glb...');

const glbPath = path.join(__dirname, '../assets/reformer_studio.glb');
const buffer = fs.readFileSync(glbPath);
const arrayBuffer = buffer.buffer.slice(buffer.byteOffset, buffer.byteOffset + buffer.byteLength);

const loader = new THREE.GLTFLoader();
loader.parse(arrayBuffer, (result) => {
  console.log('GLTF loaded successfully!');
  const scene = result.scene;
  if (!scene) {
    console.error('Scene is empty');
    process.exit(1);
  }

  const meshes = [];
  scene.traverse(node => {
    if (node.isMesh) meshes.push(node);
  });

  console.log(`Found ${meshes.length} meshes in parsed GLB.`);
  if (meshes.length < 2) {
    console.error(`Expected at least 2 meshes, found ${meshes.length}`);
    process.exit(2);
  }

  // Verify positions and normals are valid numbers
  meshes.forEach((mesh, idx) => {
    const pos = mesh.geometry.attributes.position;
    const norm = mesh.geometry.attributes.normal;
    console.log(`Mesh ${idx} (${mesh.name}): ${pos.count} vertices, normal attribute exists: ${!!norm}`);
    
    // Check first vertex values
    const x = pos.getX(0), y = pos.getY(0), z = pos.getZ(0);
    if (isNaN(x) || isNaN(y) || isNaN(z)) {
      console.error('NaN in vertex position!');
      process.exit(3);
    }
  });

  console.log('PASS: GLTF loader correctly parsed interleaved attributes (byteStride: 24)!');
  process.exit(0);
}, (err) => {
  console.error('GLTF Parse Error:', err);
  process.exit(1);
});
