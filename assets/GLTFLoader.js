// Standalone GLTF / GLB binary loader for OpenBreak PBR Reformer (UX-03)
// Fully supports interleaved attributes (byteStride: 24 with position at offset 0, normal at offset 12)
THREE.GLTFLoader = class {
  constructor() {}
  load(url, onLoad, onProgress, onError) {
    if (typeof fetch === 'undefined') {
      if (onError) onError(new Error('Fetch API not available'));
      return;
    }
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
      const meshObjects = (gltf.meshes || []).map(m => {
        const primGroup = new THREE.Group();
        primGroup.name = m.name;
        (m.primitives || []).forEach(prim => {
          const geom = new THREE.BufferGeometry();

          // Positions (Accessor POSITION)
          const posAcc = gltf.accessors[prim.attributes.POSITION];
          const posBv = gltf.bufferViews[posAcc.bufferView];
          const stride = posBv.byteStride || 12;

          const posArr = new Float32Array(posAcc.count * 3);
          const posDataView = new DataView(binData, posBv.byteOffset + (posAcc.byteOffset || 0));
          for (let i = 0; i < posAcc.count; i++) {
            const byteOffset = i * stride;
            posArr[i * 3 + 0] = posDataView.getFloat32(byteOffset + 0, true);
            posArr[i * 3 + 1] = posDataView.getFloat32(byteOffset + 4, true);
            posArr[i * 3 + 2] = posDataView.getFloat32(byteOffset + 8, true);
          }
          geom.setAttribute('position', new THREE.BufferAttribute(posArr, 3));

          // Normals (Accessor NORMAL)
          if (prim.attributes.NORMAL !== undefined) {
            const normAcc = gltf.accessors[prim.attributes.NORMAL];
            const normBv = gltf.bufferViews[normAcc.bufferView];
            const normStride = normBv.byteStride || 12;

            const normArr = new Float32Array(normAcc.count * 3);
            const normDataView = new DataView(binData, normBv.byteOffset + (normAcc.byteOffset || 0));
            for (let i = 0; i < normAcc.count; i++) {
              const byteOffset = i * normStride;
              normArr[i * 3 + 0] = normDataView.getFloat32(byteOffset + 0, true);
              normArr[i * 3 + 1] = normDataView.getFloat32(byteOffset + 4, true);
              normArr[i * 3 + 2] = normDataView.getFloat32(byteOffset + 8, true);
            }
            geom.setAttribute('normal', new THREE.BufferAttribute(normArr, 3));
          }

          // Indices
          if (prim.indices !== undefined) {
            const idxAcc = gltf.accessors[prim.indices];
            const idxBv = gltf.bufferViews[idxAcc.bufferView];
            const idxArr = new Uint16Array(binData, idxBv.byteOffset + (idxAcc.byteOffset || 0), idxAcc.count);
            geom.setIndex(new THREE.BufferAttribute(idxArr, 1));
          }

          const mat = materials[prim.material] || new THREE.MeshStandardMaterial();
          const mesh = new THREE.Mesh(geom, mat);
          mesh.name = m.name;
          primGroup.add(mesh);
        });
        return primGroup;
      });

      // Parse Node Hierarchy if defined
      if (Array.isArray(gltf.nodes) && gltf.nodes.length > 0) {
        const parsedNodes = gltf.nodes.map(n => {
          const nodeObj = new THREE.Group();
          nodeObj.name = n.name || 'GLTFNode';
          if (n.translation) nodeObj.position.fromArray(n.translation);
          if (n.rotation) nodeObj.quaternion.fromArray(n.rotation);
          if (n.scale) nodeObj.scale.fromArray(n.scale);
          if (n.mesh !== undefined && meshObjects[n.mesh]) {
            nodeObj.add(meshObjects[n.mesh]);
          }
          return nodeObj;
        });

        // Wire children
        gltf.nodes.forEach((n, idx) => {
          if (Array.isArray(n.children)) {
            n.children.forEach(childIdx => {
              if (parsedNodes[childIdx]) {
                parsedNodes[idx].add(parsedNodes[childIdx]);
              }
            });
          }
        });

        const sceneDef = (gltf.scenes && gltf.scenes[gltf.scene || 0]) || { nodes: [0] };
        (sceneDef.nodes || []).forEach(rootIdx => {
          if (parsedNodes[rootIdx]) {
            group.add(parsedNodes[rootIdx]);
          }
        });
      } else {
        meshObjects.forEach(mObj => group.add(mObj));
      }

      if (onLoad) onLoad({ scene: group, gltf });
    } catch (e) {
      if (onError) onError(e);
    }
  }
};
