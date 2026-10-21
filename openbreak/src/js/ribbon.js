/** Open Break — seamless parabolic film strip. Exactly one animation driver. */
export class ParabolicRibbon {
  constructor(viewportId, trackId) {
    this.viewport=document.getElementById(viewportId);
    this.track=document.getElementById(trackId);
    if(!this.viewport||!this.track)return;
    this.motion=window.matchMedia('(prefers-reduced-motion: reduce)');
    this.originals=[...this.track.querySelectorAll('.ribbon-card')];
    this.originals.forEach(card=>{
      const clone=card.cloneNode(true);
      clone.removeAttribute('id');clone.setAttribute('aria-hidden','true');
      this.track.appendChild(clone);
    });
    this.cards=[...this.track.querySelectorAll('.ribbon-card')];
    this.offset=0;this.target=0;this.velocity=0;this.autoSpeed=30;
    this.isDragging=false;this.hover=false;this.visible=true;this.paused=false;this.lastTime=performance.now();
    this.measure();
    this.init();
  }
  measure(){
    this.positionCache=this.cards.map(card=>({element:card,left:card.offsetLeft,width:card.offsetWidth}));
    this.period=this.cards[this.originals.length]?.offsetLeft-this.cards[0]?.offsetLeft || this.track.scrollWidth/2;
  }
  init(){
    this.viewport.setAttribute('tabindex','0');
    this.viewport.setAttribute('aria-label','Galería de escenas de estudio. Desplázate con las flechas o arrastra para explorar.');
    this.viewport.addEventListener('pointerdown',e=>{
      if(e.button!==0)return;
      this.isDragging=true;this.startX=e.clientX;this.startOffset=this.offset;this.lastX=e.clientX;this.lastPointerTime=performance.now();this.velocity=0;
      this.viewport.setPointerCapture?.(e.pointerId);
    });
    this.viewport.addEventListener('pointermove',e=>{
      if(!this.isDragging)return;
      const now=performance.now(),dt=Math.max(now-this.lastPointerTime,1);
      this.target=this.startOffset-(e.clientX-this.startX);
      this.velocity=Math.max(-1100,Math.min(1100,(this.lastX-e.clientX)/dt*1000));
      this.lastX=e.clientX;this.lastPointerTime=now;
    });
    const release=()=>{this.isDragging=false;};
    this.viewport.addEventListener('pointerup',release);
    this.viewport.addEventListener('pointercancel',release);
    this.viewport.addEventListener('mouseenter',()=>this.hover=true);
    this.viewport.addEventListener('mouseleave',()=>this.hover=false);
    this.viewport.addEventListener('keydown',e=>{
      if(e.key==='ArrowRight'||e.key==='ArrowLeft'){
        e.preventDefault();this.velocity=e.key==='ArrowRight'?350:-350;
        this.paused=true;this.updateButton();
      }
    });
    this.pauseButton=document.getElementById('pauseRibbonButton');
    this.pauseButton?.addEventListener('click',()=>{this.paused=!this.paused;this.velocity=0;this.updateButton();});
    this.updateButton();
    new ResizeObserver(()=>this.measure()).observe(this.viewport);
    if('IntersectionObserver'in window)new IntersectionObserver(entries=>{this.visible=entries[0].isIntersecting;},{threshold:.03}).observe(this.viewport);
    document.addEventListener('visibilitychange',()=>{this.lastTime=performance.now();});
    requestAnimationFrame(t=>this.loop(t));
  }
  updateButton(){if(this.pauseButton){const stopped=this.paused||this.motion.matches;this.pauseButton.textContent=stopped?'Reanudar movimiento':'Pausar movimiento';this.pauseButton.setAttribute('aria-pressed',String(stopped));}}
  loop(t){
    const dt=Math.min((t-this.lastTime)/1000,.05);this.lastTime=t;
    if(this.visible&&!document.hidden){
      if(this.isDragging)this.offset+=(this.target-this.offset)*Math.min(1,dt*22);
      else if(Math.abs(this.velocity)>5){this.offset+=this.velocity*dt;this.velocity*=Math.pow(.87,dt*60);}
      else if(!this.paused&&!this.motion.matches&&!this.hover)this.offset+=this.autoSpeed*dt;
      if(this.period>0){this.offset=((this.offset%this.period)+this.period)%this.period;}
      this.track.style.transform=`translate3d(${-this.offset}px,0,0)`;
      const center=this.viewport.clientWidth/2;
      const scale=Math.max(this.viewport.clientWidth*.52,1);
      this.positionCache.forEach(({element,left,width})=>{
        const norm=Math.max(-1.6,Math.min(1.6,(left-this.offset+width/2-center)/scale));
        element.style.transform=`translate3d(0,0,${-norm*norm*115}px) rotateY(${-norm*13}deg)`;
      });
    }
    requestAnimationFrame(next=>this.loop(next));
  }
}
