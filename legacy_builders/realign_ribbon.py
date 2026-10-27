with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Change ribbon-track position in CSS from left: 50% to left: 0
c = c.replace('position: absolute;\n      left: 50%;', 'position: absolute;\n      left: 0;')

# In JS, let currentX be offsetAccumulator with a starting offset that puts cards across the entire viewport
old_formula = '''      // Center the middle of the cards array (card 8) at screen center
      const centerBase = -(cardWidthWithGap * 8); 
      const currentX = centerBase + offsetAccumulator;'''

new_formula = '''      // Card 0 starts near left: -100px so cards span horizontally from left to right edge
      const screenShift = (window.innerWidth - (cardWidthWithGap * 8)) / 2;
      const currentX = screenShift + offsetAccumulator;'''

c = c.replace(old_formula, new_formula)

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Realigned ribbon across entire viewport!')
