/** Open Break — workflow as a tactile, accessible explanation, not a fake database. */
export class StudioWorkflowCanvas {
  constructor(containerId) {
    this.container=document.getElementById(containerId);
    if(!this.container) return;
    this.nodes=[...this.container.querySelectorAll('.workflow-node')];
    this.svg=this.container.querySelector('.workflow-wires-svg');
    this.active=0;
    this.summaries=[
      ['Tu clase, en orden.','El estudio publica sus lugares y las alumnas eligen un horario.'],
      ['Cada lugar tiene su reserva.','La plaza elegida pasa a ocupada. Otra alumna no puede recibirla en la misma clase.'],
      ['Una cancelación abre la puerta.','El espacio libre puede ofrecerse a quien está esperando, según las reglas del estudio.'],
      ['La llegada, sin filas.','Recepción visualiza la reserva y confirma la asistencia de la alumna.']
    ];
    this.wires=['wire-1-2','wire-2-3','wire-3-4'].map(id=>document.getElementById(id));
    this.nodes.forEach((node,i)=>{
      node.addEventListener('click',()=>{if(!node.dataset.justDragged)this.select(i);});
      node.addEventListener('keydown',e=>{
        if(e.key==='ArrowRight'||e.key==='ArrowDown'){e.preventDefault();this.select((i+1)%this.nodes.length);this.nodes[this.active].focus();}
        if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();this.select((i+this.nodes.length-1)%this.nodes.length);this.nodes[this.active].focus();}
      });
    });
    document.getElementById('workflowPrev')?.addEventListener('click',()=>this.select((this.active+this.nodes.length-1)%this.nodes.length));
    document.getElementById('workflowNext')?.addEventListener('click',()=>this.select((this.active+1)%this.nodes.length));
    this.setupDrag();
    this.select(0);
    this.resizeObserver=typeof ResizeObserver!=='undefined'?new ResizeObserver(()=>this.scheduleWires()):null;
    this.resizeObserver?.observe(this.container);
    this.nodes.forEach(el=>this.resizeObserver?.observe(el));
    window.addEventListener('resize',()=>this.scheduleWires(),{passive:true});
    this.scheduleWires();
  }
  select(index){
    this.active=index;
    this.nodes.forEach((n,i)=>n.setAttribute('aria-pressed',String(i===index)));
    const title=document.getElementById('workflowActiveTitle');
    const desc=document.getElementById('workflowActiveDescription');
    const number=document.getElementById('workflowActiveIndex');
    if(title)title.textContent=this.summaries[index][0];
    if(desc)desc.textContent=this.summaries[index][1];
    if(number)number.textContent=String(index+1).padStart(2,'0');
    this.wires.forEach((path,i)=>{if(path){path.style.stroke=i<index?'#E7BC6C':'#A46C57';path.style.opacity=i<=index?1:.5;}});
  }
  scheduleWires(){
    if(this.wireRaf)cancelAnimationFrame(this.wireRaf);
    this.wireRaf=requestAnimationFrame(()=>this.updateWires());
  }
  updateWires(){
    if(!this.svg||window.matchMedia('(max-width:900px)').matches)return;
    const base=this.container.getBoundingClientRect();
    this.wires.forEach((path,i)=>{
      if(!path)return;
      const a=this.nodes[i].getBoundingClientRect(),b=this.nodes[i+1].getBoundingClientRect();
      const aCenter=a.left+a.width/2, bCenter=b.left+b.width/2;
      const forward=bCenter>=aCenter;
      const x1=(forward?a.right:a.left)-base.left, x2=(forward?b.left:b.right)-base.left;
      const y1=a.top+a.height/2-base.top, y2=b.top+b.height/2-base.top;
      const arc=Math.max(40,Math.abs(x2-x1)*.46)*(forward?1:-1);
      path.setAttribute('d',`M${x1} ${y1} C${x1+arc} ${y1}, ${x2-arc} ${y2}, ${x2} ${y2}`);
    });
  }
  setupDrag(){
    if(window.matchMedia('(pointer:coarse)').matches)return; // click/tap remains available on touch
    this.nodes.forEach(node=>{
      let drag=null;
      node.addEventListener('pointerdown',e=>{
        if(e.button!==0||window.matchMedia('(max-width:900px)').matches)return;
        drag={x:e.clientX,y:e.clientY,l:node.offsetLeft,t:node.offsetTop,moved:false};
        node.setPointerCapture?.(e.pointerId);
      });
      node.addEventListener('pointermove',e=>{
        if(!drag)return;
        const dx=e.clientX-drag.x,dy=e.clientY-drag.y;
        if(Math.abs(dx)+Math.abs(dy)>7)drag.moved=true;
        if(!drag.moved)return;
        node.classList.add('is-dragging');
        const maxX=this.container.clientWidth-node.offsetWidth,maxY=this.container.clientHeight-node.offsetHeight;
        node.style.left=`${Math.max(4,Math.min(maxX-4,drag.l+dx))}px`;
        node.style.top=`${Math.max(4,Math.min(maxY-4,drag.t+dy))}px`;
        this.scheduleWires();
      });
      const stop=()=>{
        if(drag?.moved){node.dataset.justDragged='1';setTimeout(()=>delete node.dataset.justDragged,0);}
        drag=null;node.classList.remove('is-dragging');
      };
      node.addEventListener('pointerup',stop);node.addEventListener('pointercancel',stop);
    });
  }
}
