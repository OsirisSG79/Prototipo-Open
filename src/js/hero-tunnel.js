/**
 * Open Break / Spatial Tunnel (Sprint 2 / V7-03 Resolution)
 * Continuous cylindrical orbit with hermite spatial trajectory.
 * Both entry horizon (t near 0) AND exit foreground (t near 1) smoothly crossfade
 * and scale gracefully beyond viewport perimeter, eliminating boundary pops completely.
 */
(()=>{'use strict';
  const root=document.getElementById('obTunnel');if(!root)return;
  const cards=[...root.querySelectorAll('.tunnel-panel')];
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
  const pause=document.getElementById('obTunnelPause');
  let phase=0,pointer=0,target=0,down=false,pressX=0,dragPhase=0,paused=false,visible=true,last=performance.now();
  root.tabIndex=0;
  root.setAttribute('aria-roledescription','galería visual animada');
  const widths=()=>window.innerWidth;
  function paint(){
    const w=widths(),mobile=w<601,mid=w<1000;
    const limit=mobile?Math.min(195,w*.54):mid?w*.50:w*.48;
    cards.forEach((el,i)=>{
      const side=i<6?-1:1,k=i%6;
      // Continuous wrap with period 6
      const rawPos=((k+phase/2.1)%6+6)%6;
      const t=rawPos/5.999;
      // Hermite smooth cubic ease for spatial depth distribution
      const eased=t*t*(3-2*t);
      
      // X trajectory smoothly expands outward as it reaches the observer
      const x=side*((mobile?35:70)+(limit-(mobile?35:70))*eased)+(pointer*(mobile?6:14)*(1-t));
      const z=-380+eased*520; // z from -380px (deep background) to +140px (past screen threshold)
      const y=(mobile?34:42)+(1-eased)*(mobile?-3:-6)+(i%3-1)*(mobile?2:4);
      const rot=side*(-18+eased*24);
      const scale=(mobile?.25:.30)+(mobile?.54:.92)*eased;
      
      // Bilateral boundary smoothing:
      // 1. Entry fade at horizon (t: 0.0 -> 0.15)
      const entryFade = Math.min(1, Math.max(0, t / 0.15));
      // 2. Exit fade past camera near-plane (t: 0.85 -> 1.0)
      const exitFade = Math.min(1, Math.max(0, (1 - t) / 0.15));
      // Combined window envelope eliminating both entry and exit pops
      const envelope = entryFade * exitFade;
      const finalOpacity = Math.min(1, Math.max(0, (0.15 + eased * 0.85) * envelope));

      el.style.setProperty('--x',x.toFixed(2)+'px');
      el.style.setProperty('--y',y.toFixed(2)+'%');
      el.style.setProperty('--z',z.toFixed(1)+'px');
      el.style.setProperty('--r',rot.toFixed(1)+'deg');
      el.style.setProperty('--s',scale.toFixed(3));
      el.style.setProperty('--o',finalOpacity.toFixed(3));
      el.style.zIndex=String(3+Math.round(eased*70));
    });
  }
  function setPause(value){paused=value;pause?.setAttribute('aria-pressed',String(paused));pause?.setAttribute('aria-label',paused?'Reanudar galería':'Pausar movimiento de la galería');if(pause)pause.textContent=paused?'▶':'Ⅱ';}
  pause?.addEventListener('click',()=>setPause(!paused));
  root.addEventListener('pointerdown',e=>{if(e.target.closest('button,a'))return;if(e.pointerType==='mouse'&&e.button!==0)return;down=true;pressX=e.clientX;dragPhase=phase;root.classList.add('is-dragging');root.setPointerCapture?.(e.pointerId);});
  root.addEventListener('pointermove',e=>{if(!down){target=Math.max(-1,Math.min(1,(e.clientX-innerWidth/2)/(innerWidth/2)));return;} phase=dragPhase+(pressX-e.clientX)/(innerWidth<600?85:175);paint();});
  const release=()=>{down=false;root.classList.remove('is-dragging');};
  root.addEventListener('pointerup',release);root.addEventListener('pointercancel',release);
  root.addEventListener('pointerleave',()=>{target=0;});
  root.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){phase+=(e.key==='ArrowRight'?.35:-.35);paint();e.preventDefault();}});
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;},{threshold:.01}).observe(root);
  function loop(now){const dt=Math.min(.06,(now-last)/1000);last=now;pointer+=(target-pointer)*Math.min(1,dt*3.6);if(!down&&!paused&&!reduce.matches&&visible&&!document.hidden)phase+=dt*.115;if(visible||reduce.matches)paint();requestAnimationFrame(loop);}
  window.addEventListener('resize',paint,{passive:true});
  reduce.addEventListener?.('change',()=>{setPause(reduce.matches);paint();});
  if(reduce.matches)setPause(true);
  paint();requestAnimationFrame(loop);
})();
