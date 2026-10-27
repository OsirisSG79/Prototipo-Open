with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the old ribbon mousemove handler that was overwriting transform
old_handler = '''    const ribbonStage = document.getElementById('ribbonStage');
    const ribbonTrack = document.getElementById('ribbonTrack');

    if (ribbonStage && ribbonTrack) {
      window.addEventListener('mousemove', (e) => {
        const xOffset = (e.clientX / window.innerWidth - 0.5) * 36;
        const yOffset = (e.clientY / window.innerHeight - 0.5) * 14;
        ribbonTrack.style.transform = `rotateY(${xOffset * 0.4}deg) rotateX(${-yOffset * 0.5}deg) translateX(${xOffset * 1.2}px)`;
      });
    }'''

new_conveyor_engine = '''    /* ====================================================================
       AUTHENTIC MELIUS CONTINUOUS CONVEYOR ENGINE (PHYSICS & PARABOLA)
       ==================================================================== */
    const ribbonTrack = document.getElementById('ribbonTrack');
    const ribbonCards = document.querySelectorAll('.melius-continuous-card');

    let ribbonScrollPos = -600; // centered offset
    const cardWidthWithGap = 211; // 195px + 16px gap
    const totalLoopWidth = cardWidthWithGap * 8; // width of 8 cards
    let autoSpeed = 0.9;
    let targetSpeed = autoSpeed;
    let mouseTiltX = 0, mouseTiltY = 0;

    window.addEventListener('mousemove', (e) => {
      mouseTiltX = (e.clientX / window.innerWidth - 0.5) * 24;
      mouseTiltY = (e.clientY / window.innerHeight - 0.5) * 14;
    });

    let lastScroll = window.scrollY;
    window.addEventListener('scroll', () => {
      const delta = window.scrollY - lastScroll;
      lastScroll = window.scrollY;
      targetSpeed = autoSpeed + delta * 0.2;
      setTimeout(() => { targetSpeed = autoSpeed; }, 150);
    });

    function updateParabolicCards() {
      const screenCenter = window.innerWidth / 2;

      ribbonCards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const cardCenter = rect.left + rect.width / 2;
        const normDist = (cardCenter - screenCenter) / (window.innerWidth / 2);
        
        // Parabolic formula for outward curvature
        const clamped = Math.max(-1.6, Math.min(1.6, normDist));
        const rotY = clamped * 26;
        const transZ = Math.pow(Math.abs(clamped), 1.5) * 35;
        const rotX = -mouseTiltY * 0.4;

        if (!card.matches(':hover')) {
          card.style.transform = `rotateY(${rotY}deg) rotateX(${rotX}deg) translateZ(${transZ}px)`;
        }
      });
    }

    function animateConveyor() {
      ribbonScrollPos -= targetSpeed;
      if (Math.abs(ribbonScrollPos) >= totalLoopWidth * 2) {
        ribbonScrollPos += totalLoopWidth;
      }

      if (ribbonTrack) {
        ribbonTrack.style.transform = `translateX(${ribbonScrollPos}px) rotateY(${mouseTiltX * 0.25}deg)`;
      }

      updateParabolicCards();
      requestAnimationFrame(animateConveyor);
    }
    requestAnimationFrame(animateConveyor);'''

c = c.replace(old_handler, new_conveyor_engine)

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Replaced ribbon handler with continuous physics engine!")
