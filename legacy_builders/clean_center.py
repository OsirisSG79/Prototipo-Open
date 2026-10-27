with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace ribbon-stage CSS so it's a normal centered container
old_stage_css = '''.ribbon-stage {
      position: relative;
      width: 100vw;
      left: 50%;
      right: 50%;
      margin-left: -50vw;
      margin-right: -50vw;
      height: 380px;
      margin-top: 15px;
      margin-bottom: 25px;
      perspective: 1400px;
      overflow: hidden;
      z-index: 5;
    }
    .ribbon-track {
      position: absolute;
      left: 0;
      top: 50px;
      display: flex;
      gap: 16px;
      width: max-content;
      transform-style: preserve-3d;
      will-change: transform;
      cursor: grab;
    }'''

new_stage_css = '''.ribbon-stage {
      position: relative;
      width: 100%;
      max-width: 100vw;
      height: 380px;
      margin: 15px auto 25px;
      perspective: 1400px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 5;
    }
    .ribbon-track {
      display: flex;
      gap: 16px;
      width: max-content;
      transform-style: preserve-3d;
      will-change: transform;
      cursor: grab;
      align-items: center;
    }'''

c = c.replace(old_stage_css, new_stage_css)

# Update JavaScript to translate ribbonTrack smoothly with infinite loop around center
old_anim_loop = '''    function animateConveyor() {
      offsetAccumulator -= targetSpeed;
      if (Math.abs(offsetAccumulator) >= totalLoopWidth) {
        offsetAccumulator += totalLoopWidth;
      }

      // Card 0 starts near left: -100px so cards span horizontally from left to right edge
      const screenShift = -950;
      const currentX = screenShift + offsetAccumulator;

      if (ribbonTrack) {
        ribbonTrack.style.transform = `translateX(${currentX}px) rotateY(${mouseTiltX * 0.25}deg)`;
      }

      updateParabolicCards();
      requestAnimationFrame(animateConveyor);
    }'''

new_anim_loop = '''    let continuousX = 0;
    function animateConveyor() {
      continuousX -= targetSpeed;
      if (Math.abs(continuousX) >= totalLoopWidth) {
        continuousX += totalLoopWidth;
      }

      if (ribbonTrack) {
        ribbonTrack.style.transform = `translateX(${continuousX}px) rotateY(${mouseTiltX * 0.25}deg)`;
      }

      updateParabolicCards();
      requestAnimationFrame(animateConveyor);
    }'''

c = c.replace(old_anim_loop, new_anim_loop)

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Clean center applied!')
