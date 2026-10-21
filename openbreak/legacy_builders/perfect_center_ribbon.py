with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect how the track is translated
old_js = '''    const ribbonTrack = document.getElementById('ribbonTrack');
    const ribbonCards = document.querySelectorAll('.melius-continuous-card');

    let ribbonScrollPos = -(211 * 4); // centered offset
    const cardWidthWithGap = 211; // 195px + 16px gap
    const totalLoopWidth = cardWidthWithGap * 8; // width of 8 cards
    let autoSpeed = 0.9;
    let targetSpeed = autoSpeed;
    let mouseTiltX = 0, mouseTiltY = 0;'''

# In order to center 16 cards across left: 50%, we shift track by -half the total width plus offset
new_js = '''    const ribbonTrack = document.getElementById('ribbonTrack');
    const ribbonCards = document.querySelectorAll('.melius-continuous-card');

    const cardWidthWithGap = 211; // 195px + 16px gap
    const totalLoopWidth = cardWidthWithGap * 8; // width of 8 cards
    let offsetAccumulator = 0;
    let autoSpeed = 0.85;
    let targetSpeed = autoSpeed;
    let mouseTiltX = 0, mouseTiltY = 0;'''

c = c.replace(old_js, new_js)

old_anim = '''    function animateConveyor() {
      ribbonScrollPos -= targetSpeed;
      if (Math.abs(ribbonScrollPos) >= totalLoopWidth * 2) {
        ribbonScrollPos += totalLoopWidth;
      }

      if (ribbonTrack) {
        ribbonTrack.style.transform = `translateX(${ribbonScrollPos}px) rotateY(${mouseTiltX * 0.25}deg)`;
      }

      updateParabolicCards();
      requestAnimationFrame(animateConveyor);
    }'''

new_anim = '''    function animateConveyor() {
      offsetAccumulator -= targetSpeed;
      if (Math.abs(offsetAccumulator) >= totalLoopWidth) {
        offsetAccumulator += totalLoopWidth;
      }

      // Center the middle of the cards array (card 8) at screen center
      const centerBase = -(cardWidthWithGap * 8); 
      const currentX = centerBase + offsetAccumulator;

      if (ribbonTrack) {
        ribbonTrack.style.transform = `translateX(${currentX}px) rotateY(${mouseTiltX * 0.25}deg)`;
      }

      updateParabolicCards();
      requestAnimationFrame(animateConveyor);
    }'''

c = c.replace(old_anim, new_anim)

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Perfect symmetric center applied!')
