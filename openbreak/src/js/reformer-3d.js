/**
 * OPEN BREAK — procedural Reformer product study.
 * Deliberate lightweight prototype; NOT a photorealistic CAD/Blender GLB asset.
 * Walnut frame, carriage, runners, hinges, spring coils, risers, pulleys and ropes.
 * It degrades to photography if WebGL is unavailable.
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
    this.init();
  }
  init(){
    try {
      if(typeof THREE==='undefined')throw new Error('Three.js no cargó');
      if(!this.canvas.getContext('webgl')&&!this.canvas.getContext('experimental-webgl'))throw new Error('WebGL no disponible');
      this.setup();this.buildModel();this.bind();this.resize();
      this.observer=new IntersectionObserver(entries=>{this.visible=entries[0].isIntersecting;},{threshold:.06});
      this.observer.observe(this.canvas.parentElement);
      document.addEventListener('visibilitychange',()=>{this.lastFrame=performance.now();});
      this.animate();
    } catch(err){console.warn('Open Break: vista 3D sustituida por imagen:',err.message);this.fallbackMode();}
  }
  fallbackMode(){
    this.fallback?.classList.add('active');this.canvas.style.display='none';
    document.querySelectorAll('[data-reformer-control]').forEach(el=>{el.disabled=true;el.title='Controles disponibles solamente con WebGL';});
  }
  setup(){
    this.scene=new THREE.Scene();
    this.camera=new THREE.PerspectiveCamera(36,1,.1,100);
    this.camera.position.set(4.8,3.7,7.4);this.camera.lookAt(0,.52,0);
    this.renderer=new THREE.WebGLRenderer({canvas:this.canvas,antialias:true,alpha:true,powerPreference:'default'});
    this.renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.5));
    this.renderer.setClearColor(0xFFFFFF,0);
    if('outputEncoding'in this.renderer && 'sRGBEncoding'in THREE)this.renderer.outputEncoding=THREE.sRGBEncoding;
    if('toneMapping'in this.renderer && 'ACESFilmicToneMapping'in THREE)this.renderer.toneMapping=THREE.ACESFilmicToneMapping;
    if('toneMappingExposure'in this.renderer)this.renderer.toneMappingExposure=1.13;
    this.scene.add(new THREE.HemisphereLight(0xffffff,0x85735c,1.45));
    const area=new THREE.DirectionalLight(0xfff2df,2.0);area.position.set(-4,9,6);this.scene.add(area);
    const rim=new THREE.DirectionalLight(0xe6eef4,1.05);rim.position.set(5,3,-5);this.scene.add(rim);
    const bounce=new THREE.DirectionalLight(0xffffff,.5);bounce.position.set(1,2,6);this.scene.add(bounce);
    this.model=new THREE.Group();this.scene.add(this.model);
    this.materials={
      walnut:new THREE.MeshStandardMaterial({color:0x68442a,roughness:.59,metalness:.01}),
      edge:new THREE.MeshStandardMaterial({color:0x3c2a20,roughness:.69}),
      brushed:new THREE.MeshStandardMaterial({color:0xb6b6af,roughness:.28,metalness:.76}),
      steel:new THREE.MeshStandardMaterial({color:0x666a69,roughness:.23,metalness:.87}),
      upholstery:new THREE.MeshStandardMaterial({color:0x292b28,roughness:.9,metalness:0}),
      stitching:new THREE.MeshStandardMaterial({color:0xb8b1a2,roughness:1}),
      rope:new THREE.MeshStandardMaterial({color:0xbab09f,roughness:.91}),
      orange:new THREE.MeshStandardMaterial({color:0xdb582f,metalness:.53,roughness:.31}),
      yellow:new THREE.MeshStandardMaterial({color:0xb5a453,metalness:.53,roughness:.31}),
      rubber:new THREE.MeshStandardMaterial({color:0x151818,roughness:.82})
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
    const part=this.part(new THREE.CylinderGeometry(r,r,h,20),mat,x,y,z,parent);
    if(rotation)part.rotation.set(...rotation);
    return part;
  }
  helix(radius,length,turns,x,y,z,mat){
    class HelixCurve extends THREE.Curve{
      getPoint(t){return new THREE.Vector3(Math.cos(t*Math.PI*2*turns)*radius,Math.sin(t*Math.PI*2*turns)*radius,length*(t-.5));}
    }
    return this.part(new THREE.TubeGeometry(new HelixCurve(),turns*14,.013,7,false),mat,x,y,z);
  }
  buildModel(){
    const m=this.materials;
    // Shadow plane: quiet product-stage context without texture requests.
    const floor=this.part(new THREE.CircleGeometry(3.5,70),new THREE.MeshBasicMaterial({color:0xDEDCD4,transparent:true,opacity:.09,depthWrite:false}),0,-.03,0,this.scene);
    floor.rotation.x=-Math.PI/2;floor.scale.set(1,.72,1);
    // Actual open frame, not one giant block: four walnut stringers and shaped endcaps.
    for(const x of [-.79,.79]){
      this.beam(.145,.19,4.84,x,.56,0,m.walnut);
      this.beam(.085,.045,4.65,x,.68,0,m.edge);
      this.beam(.055,.055,4.58,x*.88,.765,0,m.brushed);
      for(const z of [-2.05,2.05]){
        this.beam(.11,.48,.13,x,.25,z,m.edge);
        this.cylinder(.08,.08,x,.065,z,m.rubber);
      }
      this.cylinder(.053,4.55,x,.39,0,m.brushed,[Math.PI/2,0,0]);
    }
    for(const z of [-2.34,2.34]){
      this.beam(1.72,.17,.19,0,.56,z,m.walnut);
      this.beam(1.60,.035,.08,0,.69,z,m.brushed);
    }
    // Carriage with two-layer leather cushion, edge piping, bearings and headrest.
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
    // Articulated foot bar with side uprights and rubber grip.
    for(const x of [-.75,.75]){
      this.tube([[x,.68,1.84],[x,.92,2.05],[x,1.29,2.18]],.031,m.brushed);
      this.cylinder(.08,.11,x,.69,1.84,m.steel,[Math.PI/2,0,0]);
    }
    this.cylinder(.047,1.58,0,1.29,2.18,m.rubber,[0,0,Math.PI/2]);
    for(const x of [-.84,.84])this.cylinder(.056,.14,x,1.29,2.18,m.brushed,[0,0,Math.PI/2]);
    // Adjustable spring array, each coil visibly helical.
    for(let i=0;i<5;i++){
      const x=(i-2)*.225;
      this.cylinder(.027,.13,x,.67,.94,m.steel,[Math.PI/2,0,0]);
      const s=this.helix(.042,.70,14,x,.69,1.42,i===2?m.orange:m.steel);
      this.springs.push(s);
      this.cylinder(.04,.10,x,.68,1.82,m.brushed,[Math.PI/2,0,0]);
    }
    // Tower posts, sheaves and rope trajectories; real hardware silhouettes.
    for(const x of [-.64,.64]){
      this.cylinder(.036,1.16,x,1.24,-2.25,m.brushed);
      this.cylinder(.14,.09,x,1.84,-2.25,m.steel,[0,0,Math.PI/2]);
      this.cylinder(.09,.11,x,1.84,-2.25,m.rubber,[0,0,Math.PI/2]);
      this.tube([[x,1.83,-2.22],[x,2.06,-2.15],[x,2.10,-1.77],[x,1.86,-1.43]],.014,m.rope);
      this.cylinder(.023,.25,x,1.80,-1.35,m.rubber,[0,0,Math.PI/2]);
    }
    // Plaque & handles at the end of the chassis.
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
      this.carriageGroup.position.z=this.carriage;
      this.springs.forEach(s=>{s.scale.z=1+this.carriage*.32;});
      this.renderer.render(this.scene,this.camera);
    }
    requestAnimationFrame(()=>this.animate());
  }
}
