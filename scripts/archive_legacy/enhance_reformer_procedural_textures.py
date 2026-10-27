from pathlib import Path

# Add procedural canvas noise / micro-textures into reformer-3d.js to simulate realistic wood grain and brushed metal
p = Path('/home/user/openbreak/src/js/reformer-3d.js')
content = p.read_text(encoding='utf-8')

procedural_texture_helpers = """
  // UX-03: Procedural micro-texture synthesizers (Wood grain & Brushed Aluminum)
  createProceduralWoodTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#6e472a';
    ctx.fillRect(0, 0, 512, 512);
    // Draw wood grain lines
    ctx.fillStyle = '#5c3a20';
    for (let i = 0; i < 512; i += 3) {
      const w = 1 + Math.sin(i * 0.05) * 1.5;
      ctx.fillRect(0, i, 512, w);
    }
    // Add subtle organic turbulence
    const imgData = ctx.getImageData(0, 0, 512, 512);
    const data = imgData.data;
    for (let i = 0; i < data.length; i += 4) {
      const noise = (Math.random() - 0.5) * 16;
      data[i] = Math.max(0, Math.min(255, data[i] + noise));
      data[i+1] = Math.max(0, Math.min(255, data[i+1] + noise * 0.8));
      data[i+2] = Math.max(0, Math.min(255, data[i+2] + noise * 0.5));
    }
    ctx.putImageData(imgData, 0, 0);
    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 6);
    return tex;
  }

  createProceduralBrushedTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#d0d4d8';
    ctx.fillRect(0, 0, 256, 256);
    ctx.fillStyle = '#9aa0a6';
    for (let i = 0; i < 256; i += 2) {
      if (Math.random() > 0.4) {
        ctx.fillRect(i, 0, 1, 256);
      }
    }
    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    return tex;
  }
"""

old_materials = """    this.materials={
      walnut:new THREE.MeshStandardMaterial({color:0x6b4423,roughness:.58,metalness:.04}),
      steel:new THREE.MeshStandardMaterial({color:0x202428,metalness:.92,roughness:.28}),
      brushed:new THREE.MeshStandardMaterial({color:0xd7dcde,metalness:.86,roughness:.26}),
      edge:new THREE.MeshStandardMaterial({color:0x875a33,roughness:.64,metalness:.03}),
      upholstery:new THREE.MeshStandardMaterial({color:0x1b1c1e,roughness:.82,metalness:.10}),
      stitching:new THREE.MeshStandardMaterial({color:0xbdb6a7,roughness:.95}),
      rope:new THREE.MeshStandardMaterial({color:0xbdb3a1,roughness:.88}),
      orange:new THREE.MeshStandardMaterial({color:0xdb582f,metalness:.60,roughness:.26}),
      yellow:new THREE.MeshStandardMaterial({color:0xbfa94e,metalness:.60,roughness:.26}),
      rubber:new THREE.MeshStandardMaterial({color:0x121414,roughness:.78})
    };"""

new_materials = """    const woodTex = this.createProceduralWoodTexture();
    const brushedTex = this.createProceduralBrushedTexture();
    this.materials={
      walnut:new THREE.MeshStandardMaterial({map:woodTex,roughness:.52,metalness:.04}),
      steel:new THREE.MeshStandardMaterial({color:0x202428,metalness:.92,roughness:.24}),
      brushed:new THREE.MeshStandardMaterial({map:brushedTex,color:0xd7dcde,metalness:.88,roughness:.22}),
      edge:new THREE.MeshStandardMaterial({map:woodTex,roughness:.60,metalness:.03}),
      upholstery:new THREE.MeshStandardMaterial({color:0x18191b,roughness:.85,metalness:.08}),
      stitching:new THREE.MeshStandardMaterial({color:0xbdb6a7,roughness:.95}),
      rope:new THREE.MeshStandardMaterial({color:0xbdb3a1,roughness:.88}),
      orange:new THREE.MeshStandardMaterial({color:0xdb582f,metalness:.60,roughness:.26}),
      yellow:new THREE.MeshStandardMaterial({color:0xbfa94e,metalness:.60,roughness:.26}),
      rubber:new THREE.MeshStandardMaterial({color:0x121414,roughness:.78})
    };"""

if "createProceduralWoodTexture" not in content:
    target = "initMaterials(){"
    content = content.replace(target, procedural_texture_helpers + "\n  initMaterials(){\n")
    content = content.replace(old_materials, new_materials)
    p.write_text(content, encoding='utf-8')
    print("Enhanced Reformer 3D materials with procedural grain and brushed metal textures.")
