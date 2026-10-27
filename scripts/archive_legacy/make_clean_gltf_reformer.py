import json, struct
from pathlib import Path

# Construct a valid, standalone binary GLTF (.glb) containing the core Reformer frame and sliding carriage
# Spec: glTF 2.0 Binary (Magic: 0x46546C67, Version: 2)

# Vertices for a simplified Reformer Frame (outer box) and Carriage (inner box)
# Frame Box: 1.8 x 0.4 x 4.2
# Carriage Box: 1.4 x 0.15 x 2.0

def create_box_mesh(w, h, d, ox=0, oy=0, oz=0):
    # Returns 24 vertices (pos 3 floats, normal 3 floats) and 36 indices
    hw, hh, hd = w/2, h/2, d/2
    # 6 faces
    faces = [
        # Front (+Z)
        ([-hw, -hh,  hd], [ hw, -hh,  hd], [ hw,  hh,  hd], [-hw,  hh,  hd], [0, 0, 1]),
        # Back (-Z)
        ([ hw, -hh, -hd], [-hw, -hh, -hd], [-hw,  hh, -hd], [ hw,  hh, -hd], [0, 0, -1]),
        # Top (+Y)
        ([-hw,  hh,  hd], [ hw,  hh,  hd], [ hw,  hh, -hd], [-hw,  hh, -hd], [0, 1, 0]),
        # Bottom (-Y)
        ([-hw, -hh, -hd], [ hw, -hh, -hd], [ hw, -hh,  hd], [-hw, -hh,  hd], [0, -1, 0]),
        # Right (+X)
        ([ hw, -hh,  hd], [ hw, -hh, -hd], [ hw,  hh, -hd], [ hw,  hh,  hd], [1, 0, 0]),
        # Left (-X)
        ([-hw, -hh, -hd], [-hw, -hh,  hd], [-hw,  hh,  hd], [-hw,  hh, -hd], [-1, 0, 0]),
    ]
    verts = []
    indices = []
    idx_offset = 0
    for f in faces:
        p0, p1, p2, p3, n = f
        for p in [p0, p1, p2, p3]:
            verts.append((p[0]+ox, p[1]+oy, p[2]+oz, n[0], n[1], n[2]))
        indices.extend([idx_offset, idx_offset+1, idx_offset+2, idx_offset, idx_offset+2, idx_offset+3])
        idx_offset += 4
    return verts, indices

verts_frame, indices_frame = create_box_mesh(1.6, 0.35, 4.4, 0, 0.5, 0)
verts_carr, indices_carr = create_box_mesh(1.3, 0.12, 2.0, 0, 0.85, -0.2)

# Pack binary buffers
pos_norm_data = bytearray()
for v in (verts_frame + verts_carr):
    # pos x, y, z, norm nx, ny, nz
    pos_norm_data.extend(struct.pack('<ffffff', *v))

index_data = bytearray()
for idx in indices_frame:
    index_data.extend(struct.pack('<H', idx))
for idx in indices_carr:
    index_data.extend(struct.pack('<H', idx + len(verts_frame)))

# Align index data to 4 bytes
while len(index_data) % 4 != 0:
    index_data.extend(b'\x00')

buffer_bytes = pos_norm_data + index_data
while len(buffer_bytes) % 4 != 0:
    buffer_bytes.extend(b'\x00')

gltf_dict = {
    "asset": {"version": "2.0", "generator": "OpenBreak PBR Reformer Asset Pipeline"},
    "scenes": [{"nodes": [0]}],
    "nodes": [
        {"name": "ReformerRoot", "children": [1, 2]},
        {"name": "ReformerFrame", "mesh": 0},
        {"name": "ReformerCarriage", "mesh": 1}
    ],
    "meshes": [
        {
            "name": "FrameMesh",
            "primitives": [{
                "attributes": {"POSITION": 0, "NORMAL": 1},
                "indices": 2,
                "material": 0
            }]
        },
        {
            "name": "CarriageMesh",
            "primitives": [{
                "attributes": {"POSITION": 3, "NORMAL": 4},
                "indices": 5,
                "material": 1
            }]
        }
    ],
    "materials": [
        {
            "name": "WalnutTimberPBR",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.42, 0.27, 0.14, 1.0],
                "metallicFactor": 0.05,
                "roughnessFactor": 0.55
            }
        },
        {
            "name": "BlackLeatherPBR",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.10, 0.11, 0.12, 1.0],
                "metallicFactor": 0.10,
                "roughnessFactor": 0.80
            }
        }
    ],
    "accessors": [
        {"bufferView": 0, "byteOffset": 0, "componentType": 5126, "count": 24, "type": "VEC3", "max": [0.8, 0.675, 2.2], "min": [-0.8, 0.325, -2.2]},
        {"bufferView": 0, "byteOffset": 12, "componentType": 5126, "count": 24, "type": "VEC3"},
        {"bufferView": 1, "byteOffset": 0, "componentType": 5123, "count": 36, "type": "SCALAR"},
        {"bufferView": 0, "byteOffset": 24 * 24, "componentType": 5126, "count": 24, "type": "VEC3", "max": [0.65, 0.91, 0.8], "min": [-0.65, 0.79, -1.2]},
        {"bufferView": 0, "byteOffset": 24 * 24 + 12, "componentType": 5126, "count": 24, "type": "VEC3"},
        {"bufferView": 1, "byteOffset": 36 * 2, "componentType": 5123, "count": 36, "type": "SCALAR"}
    ],
    "bufferViews": [
        {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_norm_data), "byteStride": 24, "target": 34962},
        {"buffer": 0, "byteOffset": len(pos_norm_data), "byteLength": len(index_data), "target": 34963}
    ],
    "buffers": [{"byteLength": len(buffer_bytes)}]
}

json_str = json.dumps(gltf_dict).encode('utf-8')
while len(json_str) % 4 != 0:
    json_str += b' '

total_length = 12 + 8 + len(json_str) + 8 + len(buffer_bytes)
glb_header = struct.pack('<4sII', b'glTF', 2, total_length)
json_chunk_header = struct.pack('<I4s', len(json_str), b'JSON')
bin_chunk_header = struct.pack('<I4s', len(buffer_bytes), b'BIN\x00')

out_path = Path('/home/user/openbreak/assets/reformer_studio.glb')
with open(out_path, 'wb') as f:
    f.write(glb_header)
    f.write(json_chunk_header)
    f.write(json_str)
    f.write(bin_chunk_header)
    f.write(buffer_bytes)

print(f"Generated standalone binary GLB asset: {out_path} ({out_path.stat().st_size} bytes)")
