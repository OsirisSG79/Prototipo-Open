from pathlib import Path

# Provide a lightweight, self-contained GLTF / GLB binary parser for Three.js
loader_code = """
// Lightweight standalone GLTF / GLB binary loader for OpenBreak PBR Reformer (UX-03)
THREE.GLTFLoader = class {
  constructor() {}
  load(url, onLoad, onProgress, onError) {
    fetch(url)
      .then(response => {
        if (!response.ok) throw new Error('Network error loading ' + url);
        return response.arrayBuffer();
      })
      .then(buffer => this.parse(buffer, onLoad, onError))
      .catch(err => {
        if (onError) onError(err);
      });
  }
  parse(data, onLoad, onError) {
    try {
      const magic = new Uint32Array(data, 0, 1)[0];
      if (magic !== 0x46546C67) { // 'glTF' in hex
        throw new Error('Unsupported format: Not a binary glTF (.glb) file');
      }
      const jsonLen = new Uint32Array(data, 12, 1)[0];
      const jsonBytes = new Uint8Array(data, 20, jsonLen);
      const jsonStr = new TextDecoder().decode(jsonBytes);
      const gltf = JSON.parse(jsonStr);

      const binOffset = 20 + jsonLen + 8;
      const binData = data.slice(binOffset);

      const group = new THREE.Group();
      group.name = 'GLTF_Reformer_Root';

      // Parse materials
      const materials = (gltf.materials || []).map(m => {
        const pbr = m.pbrMetallicRoughness || {};
        const col = pbr.baseColorFactor || [0.8, 0.8, 0.8];
        return new THREE.MeshStandardMaterial({
          color: new THREE.Color(col[0], col[1], col[2]),
          roughness: pbr.roughnessFactor !== undefined ? pbr.roughnessFactor : 0.5,
          metalness: pbr.metallicFactor !== undefined ? pbr.metallicFactor : 0.1
        });
      });

      // Parse meshes
      (gltf.meshes || []).forEach(m => {
        (m.primitives || []).forEach(prim => {
          const geom = new THREE.BufferGeometry();

          // Positions (Accessor 0 or 3)
          const posAcc = gltf.accessors[prim.attributes.POSITION];
          const posBv = gltf.bufferViews[posAcc.bufferView];
          const posArr = new Float32Array(binData, posBv.byteOffset + (posAcc.byteOffset || 0), posAcc.count * 3);
          geom.setAttribute('position', new THREE.BufferAttribute(posArr, 3));

          // Normals (Accessor 1 or 4)
          if (prim.attributes.NORMAL !== undefined) {
            const normAcc = gltf.accessors[prim.attributes.NORMAL];
            const normBv = gltf.bufferViews[normAcc.bufferView];
            const normArr = new Float32Array(binData, normBv.byteOffset + (normAcc.byteOffset || 0), normAcc.count * 3);
            geom.setAttribute('normal', new THREE.BufferAttribute(normArr, 3));
          }

          // Indices (Accessor 2 or 5)
          if (prim.indices !== undefined) {
            const idxAcc = gltf.accessors[prim.indices];
            const idxBv = gltf.bufferViews[idxAcc.bufferView];
            const idxArr = new Uint16Array(binData, idxBv.byteOffset + (idxAcc.byteOffset || 0), idxAcc.count);
            geom.setIndex(new THREE.BufferAttribute(idxArr, 1));
          }

          const mat = materials[prim.material] || new THREE.MeshStandardMaterial();
          const mesh = new THREE.Mesh(geom, mat);
          mesh.name = m.name;
          group.add(mesh);
        });
      });

      if (onLoad) onLoad({ scene: group, gltf });
    } catch (e) {
      if (onError) onError(e);
    }
  }
};
"""

out_file = Path('/home/user/openbreak/assets/GLTFLoader.js')
out_file.write_text(loader_code, encoding='utf-8')
print("Created standalone GLTFLoader.js")
