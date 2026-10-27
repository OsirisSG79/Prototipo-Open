/**
 * OPEN BREAK — Reformer Studio Viewer (Sprint 05)
 * Realistic studio visualization with PBR materials, contact shadows, carriage glide kinematics,
 * dynamic spring elongation physics, responsive canvas handling, and graceful photography fallback.
 */
export class ReformerStudioViewer {
  constructor(canvasId,fallbackId){
    this.canvas=document.getElementById(canvasId);
    this.fallback=document.getElementById(fallbackId);
    if(!this.canvas)return;
    this.motion=window.matchMedia('(prefers-reduced-motion: reduce)');
    this.dragging=false;this.visible=false;
    this.rotation={x:.12,y:.62};this.target={x:.12,y:.62};
    this.carriage=0;this.carriageTarget=0;this.springTension=1;
    this.springs=[];
    this.carriageGroup=null;
    this.glbCarriageNode=null;
    this.glbSpringNodes=[];
    this.init();
  }
  init(){
    try {
      if(typeof THREE==='undefined')throw new Error('Three.js no cargó');
      if(!this.canvas.getContext('webgl')&&!this.canvas.getContext('experimental-webgl'))throw new Error('WebGL no disponible');
      this.setup();
      this.loadGlbOrFallback();
      this.bind();
      this.resize();
      this.observer=new IntersectionObserver(entries=>{this.visible=entries[0].isIntersecting;},{threshold:.06});
      this.observer.observe(this.canvas.parentElement);
      document.addEventListener('visibilitychange',()=>{this.lastFrame=performance.now();});
      this.animate();
    } catch(err){console.warn('Open Break: vista 3D sustituida por imagen:',err.message);this.fallbackMode();}
  }
  loadGlbOrFallback(){
    // P1-01 AUD-012 Fix: Mutually exclusive GLB load or procedural fallback (never overlay both)
    let glbLoaded = false;
    if(typeof THREE.GLTFLoader !== 'undefined' || typeof window.GLTFLoader !== 'undefined'){
      try {
        const LoaderClass = THREE.GLTFLoader || window.GLTFLoader;
        const loader = new LoaderClass();
        loader.load(
          'assets/reformer_studio.glb',
          (gltf) => {
            if(gltf && gltf.scene){
              // Clear procedural geometries if GLB loaded successfully
              if(this.proceduralGroup){
                this.model.remove(this.proceduralGroup);
                this.proceduralGroup = null;
              }
              this.glbScene = gltf.scene;
              this.model.add(this.glbScene);
              this.glbScene.scale.set(1.1, 1.1, 1.1);
              this.glbScene.position.set(0, 0.45, 0);

              // P1-01 (AUD-013) Fix: Bind GLB nodes to interactive controls
              this.glbCarriageNode = null;
              this.glbSpringNodes = [];
              this.glbScene.traverse(node => {
                const name = node.name || '';
                if (name === 'UpholsteredCarriage' || name.toLowerCase().includes('carriage')) {
                  this.glbCarriageNode = node;
                }
                if (name.toLowerCase().includes('spring') || name === 'SteelTracksAndFootbar') {
                  this.glbSpringNodes.push(node);
                }
              });
            }
          },
          undefined,
          (err) => {
            console.info('OpenBreak 3D: Procedural fallback active (GLB deferred):', err?.message || err);
          }
        );
      } catch(e) {
        console.info('OpenBreak 3D: GLTFLoader load skipped, keeping procedural studio model:', e.message);
      }
    }
    // Build procedural model as initial/baseline model (removed dynamically if GLB scene loads)
    this.buildModel();
  }
  fallbackMode(){
    this.fallback?.classList.add('active');this.canvas.style.display='none';
    document.querySelectorAll('[data-reformer-control]').forEach(el=>{el.disabled=true;el.title='Controles disponibles solamente con WebGL';});
  }
  setup(){
    this.scene=new THREE.Scene();
    this.camera=new THREE.PerspectiveCamera(36,1,.1,100);
    this.camera.position.set(4.8,3.7,7.4);this.camera.lookAt(0,.52,0);
    this.renderer=new THREE.WebGLRenderer({canvas:this.canvas,antialias:true,alpha:true,powerPreference:'high-performance'});
    this.renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.75));
    this.renderer.setClearColor(0xFFFFFF,0);
    if('outputEncoding'in this.renderer && 'sRGBEncoding'in THREE)this.renderer.outputEncoding=THREE.sRGBEncoding;
    if('toneMapping'in this.renderer && 'ACESFilmicToneMapping'in THREE)this.renderer.toneMapping=THREE.ACESFilmicToneMapping;
    if('toneMappingExposure'in this.renderer)this.renderer.toneMappingExposure=1.18;
    
    // Sophisticated 4-point studio lighting rig
    this.scene.add(new THREE.HemisphereLight(0xffffff,0x7d6f5d,1.55));
    const keyLight=new THREE.DirectionalLight(0xfff5e6,2.2);keyLight.position.set(-4.5,9.5,6.5);this.scene.add(keyLight);
    const rimLight=new THREE.DirectionalLight(0xe0f2fe,1.25);rimLight.position.set(5.5,3.2,-5.5);this.scene.add(rimLight);
    const fillLight=new THREE.DirectionalLight(0xffffff,.65);fillLight.position.set(1.2,2.4,6.2);this.scene.add(fillLight);
    const softUnderLight=new THREE.DirectionalLight(0xe8e4dc,.35);softUnderLight.position.set(0,-3,0);this.scene.add(softUnderLight);

    this.model=new THREE.Group();this.scene.add(this.model);
    this.materials={
      walnut:new THREE.MeshStandardMaterial({color:0x5e3a21,roughness:.48,metalness:.02}),
      edge:new THREE.MeshStandardMaterial({color:0x342218,roughness:.58}),
      brushed:new THREE.MeshStandardMaterial({color:0xbab8b2,roughness:.24,metalness:.82}),
      steel:new THREE.MeshStandardMaterial({color:0x6c7070,roughness:.20,metalness:.90}),
      upholstery:new THREE.MeshStandardMaterial({color:0x222422,roughness:.85,metalness:0}),
      stitching:new THREE.MeshStandardMaterial({color:0xbdb6a7,roughness:.95}),
      rope:new THREE.MeshStandardMaterial({color:0xbdb3a1,roughness:.88}),
      orange:new THREE.MeshStandardMaterial({color:0xdb582f,metalness:.60,roughness:.26}),
      yellow:new THREE.MeshStandardMaterial({color:0xbfa94e,metalness:.60,roughness:.26}),
      rubber:new THREE.MeshStandardMaterial({color:0x121414,roughness:.78})
    };
  }
  part(geometry,material,x=0,y=0,z=0,parent=this.model){
    const mesh=new THREE.Mesh(geometry,material);mesh.position.set(x,y,z);parent.add(mesh);return mesh;
  }
  beam(w,h,l,x,y,z,mat,parent){return this.part(new THREE.BoxGeometry(w,h,l),mat,x,y,z,parent||this.model);}
  tube(points,r,material,parent=this.model){
    const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));
    return this.part(new THREE.TubeGeometry(curve,Math.max(12,points.length*8),r,8,false),material,0,0,0,parent);
  }
  cylinder(r,h,x,y,z,mat,rotation=null,parent=this.model){
    const part=this.part(new THREE.CylinderGeometry(r,r,h,24),mat,x,y,z,parent);
    if(rotation)part.rotation.set(...rotation);
    return part;
  }
  helix(radius,length,turns,x,y,z,mat){
    class HelixCurve extends THREE.Curve{
      getPoint(t){return new THREE.Vector3(Math.cos(t*Math.PI*2*turns)*radius,Math.sin(t*Math.PI*2*turns)*radius,length*(t-.5));}
    }
    return this.part(new THREE.TubeGeometry(new HelixCurve(),turns*16,.014,8,false),mat,x,y,z);
  }
  buildModel(){
    const m=this.materials;
    this.proceduralGroup = new THREE.Group();
    this.model.add(this.proceduralGroup);
    const pg = this.proceduralGroup;

    // Ambient contact shadow disk beneath the reformer chassis
    const shadowDisk=this.part(new THREE.CircleGeometry(3.6,72),new THREE.MeshBasicMaterial({color:0xBBB6A8,transparent:true,opacity:.14,depthWrite:false}),0,-.02,0,pg);
    shadowDisk.rotation.x=-Math.PI/2;shadowDisk.scale.set(1,.74,1);
    
    // Chassis rails and longitudinal structure
    for(const x of [-.79,.79]){
      this.beam(.145,.19,4.84,x,.56,0,m.walnut,pg);
      this.beam(.085,.045,4.65,x,.68,0,m.edge,pg);
      this.beam(.055,.055,4.58,x*.88,.765,0,m.brushed,pg);
      for(const z of [-2.05,2.05]){
        this.beam(.11,.48,.13,x,.25,z,m.edge,pg);
        this.cylinder(.08,.08,x,.065,z,m.rubber,null,pg);
      }
      this.cylinder(.053,4.55,x,.39,0,m.brushed,[Math.PI/2,0,0],pg);
    }
    for(const z of [-2.34,2.34]){
      this.beam(1.72,.17,.19,0,.56,z,m.walnut,pg);
      this.beam(1.60,.035,.08,0,.69,z,m.brushed);
    }
    // Carriage assembly with ergonomic padded platform, headrest and shoulder rests
    this.carriageGroup=new THREE.Group();this.model.add(this.carriageGroup);
    this.beam(1.42,.13,2.15,0,.8,-.26,m.edge,this.carriageGroup);
    this.beam(1.33,.105,2.07,0,.906,-.26,m.upholstery,this.carriageGroup);
    this.beam(1.34,.014,1.89,0,.963,-.27,m.upholstery,this.carriageGroup);
    for(const x of [-.665,.665]){
      this.beam(.015,.035,2.05,x,.947,-.26,m.stitching,this.carriageGroup);
      for(const z of [-1.16,.63]){
        this.cylinder(.115,.06,x,.705,z,m.steel,[0,0,Math.PI/2],this.carriageGroup);
      }
    }
    this.beam(.51,.08,.43,0,1.00,-1.05,m.upholstery,this.carriageGroup);
    for(const x of [-.37,.37]){
      this.beam(.23,.28,.29,x,1.11,-.94,m.upholstery,this.carriageGroup);
      this.beam(.27,.035,.33,x,1.25,-.94,m.stitching,this.carriageGroup);
    }
    // Articulated foot bar with padded rubber sleeve and locking pivots
    for(const x of [-.75,.75]){
      this.tube([[x,.68,1.84],[x,.92,2.05],[x,1.29,2.18]],.031,m.brushed);
      this.cylinder(.08,.11,x,.69,1.84,m.steel,[Math.PI/2,0,0]);
    }
    this.cylinder(.047,1.58,0,1.29,2.18,m.rubber,[0,0,Math.PI/2]);
    for(const x of [-.84,.84])this.cylinder(.056,.14,x,1.29,2.18,m.brushed,[0,0,Math.PI/2]);
    
    // Five progressive resistance spring coils (color-coded tension)
    for(let i=0;i<5;i++){
      const x=(i-2)*.225;
      this.cylinder(.027,.13,x,.67,.94,m.steel,[Math.PI/2,0,0]);
      const s=this.helix(.042,.70,14,x,.69,1.42,i===2?m.orange:m.steel);
      this.springs.push(s);
      this.cylinder(.04,.10,x,.68,1.82,m.brushed,[Math.PI/2,0,0]);
    }
    // Tower risers, pulley wheels, and braided nautical cord paths
    for(const x of [-.64,.64]){
      this.cylinder(.036,1.16,x,1.24,-2.25,m.brushed);
      this.cylinder(.14,.09,x,1.84,-2.25,m.steel,[0,0,Math.PI/2]);
      this.cylinder(.09,.11,x,1.84,-2.25,m.rubber,[0,0,Math.PI/2]);
      this.tube([[x,1.83,-2.22],[x,2.06,-2.15],[x,2.10,-1.77],[x,1.86,-1.43]],.014,m.rope);
      this.cylinder(.023,.25,x,1.80,-1.35,m.rubber,[0,0,Math.PI/2]);
    }
    // Studio metal brand plate at the foot of the carriage
    this.beam(.39,.06,.012,0,.68,2.43,m.steel);
    this.model.rotation.set(this.rotation.x,this.rotation.y,0);
  }
  bind(){
    const down=e=>{if(e.button!==0)return;this.dragging=true;this.previous={x:e.clientX,y:e.clientY};this.canvas.setPointerCapture?.(e.pointerId)};
    const move=e=>{if(!this.dragging)return;const dx=e.clientX-this.previous.x,dy=e.clientY-this.previous.y;this.target.y+=dx*.006;this.target.x=Math.max(-.27,Math.min(.56,this.target.x+dy*.006));this.previous={x:e.clientX,y:e.clientY};};
    this.canvas.addEventListener('pointerdown',down);
    this.canvas.addEventListener('pointermove',move);
    this.canvas.addEventListener('pointerup',()=>this.dragging=false);
    this.canvas.addEventListener('pointercancel',()=>this.dragging=false);
    this.canvas.setAttribute('tabindex','0');
    this.canvas.setAttribute('aria-label','Modelo tridimensional interactivo de un Reformer. Usa las flechas para girarlo.');
    this.canvas.addEventListener('keydown',e=>{const amount=.15;if(e.key==='ArrowLeft')this.target.y-=amount;else if(e.key==='ArrowRight')this.target.y+=amount;else if(e.key==='ArrowUp')this.target.x=Math.max(-.27,this.target.x-amount);else if(e.key==='ArrowDown')this.target.x=Math.min(.56,this.target.x+amount);else return;e.preventDefault();});
    this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(this.canvas.parentElement);
    this.canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();this.fallbackMode();});
  }
  resize(){
    if(!this.renderer)return;
    const rect=this.canvas.parentElement.getBoundingClientRect();
    if(rect.width<1||rect.height<1)return;
    this.camera.aspect=rect.width/rect.height;this.camera.updateProjectionMatrix();
    this.renderer.setSize(rect.width,rect.height,false);
  }
  glideCarriage(){this.carriageTarget=this.carriageTarget>.1?0:.73;}
  toggleSprings(){
    this.springTension=this.springTension===1?2:1;
    this.springs.forEach((s,i)=>{s.material=(i===2||this.springTension===2)?this.materials.orange:this.materials.steel;});
    // In GLB mode, also modulate spring materials if present
    this.glbSpringNodes.forEach(node => {
      if (node.material) {
        node.material.color?.setHex?.(this.springTension === 2 ? 0xdb582f : 0x6c7070);
      }
    });
    this.glideCarriage();
  }
  resetCamera(){this.target={x:.12,y:.62};this.carriageTarget=0;}
  animate(){
    if(this.visible&&!document.hidden&&this.renderer){
      const speed=this.motion.matches?1:.085;
      this.rotation.x+=(this.target.x-this.rotation.x)*speed;
      this.rotation.y+=(this.target.y-this.rotation.y)*speed;
      this.model.rotation.set(this.rotation.x,this.rotation.y,0);
      this.carriage+=(this.carriageTarget-this.carriage)*speed;
      // Animate procedural carriage if active
      if (this.carriageGroup) {
        this.carriageGroup.position.z=this.carriage;
      }
      // Animate GLB carriage node if active (P1-01 AUD-013)
      if (this.glbCarriageNode) {
        this.glbCarriageNode.position.z=this.carriage;
      }
      this.springs.forEach(s=>{s.scale.z=1+this.carriage*.32;});
      this.renderer.render(this.scene,this.camera);
    }
    this.rafId=requestAnimationFrame(()=>this.animate());
  }

  dispose(){
    if(this.rafId) cancelAnimationFrame(this.rafId);
    if(this.resizeObserver) this.resizeObserver.disconnect();
    if(this.renderer){
      this.renderer.dispose();
      this.renderer.forceContextLoss();
    }
    if(this.scene){
      this.scene.traverse(obj=>{
        if(obj.geometry) obj.geometry.dispose();
        if(obj.material){
          if(Array.isArray(obj.material)) obj.material.forEach(m=>m.dispose());
          else obj.material.dispose();
        }
      });
    }
  }
}