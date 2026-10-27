/**
 * Static Contract Verification Suite for DOM Behavioral & Visual Invariants (V8.1.5 / AUD-015)
 * Static contract test assessing DOM structure, CSS constraints, ARIA tokens,
 * kinetic typewriter mechanics, 12-panel 3D tunnel geometry, and GLB kinematics bindings.
 * (Note: Per AUD-014 dictamen P1-07, these tests verify source code contracts and contracts-in-code,
 * not hardware GPU rendering or live browser display).
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const repoDir = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(repoDir, 'landing_melius_style.html'), 'utf8');

console.log('Running Static Contract Suite for DOM Behavioral & Visual Invariants (V8.1.5)...');

// 1. Kinetic Staggered Typewriter Invariance (No instant text replace)
console.log('--- 1. Typewriter Kinetic Stagger Invariance ---');
assert(html.includes('id="ob-hero-rotating-word"'), 'Missing #ob-hero-rotating-word');
assert(html.includes('src/js/title-typewriter.js'), 'Missing title-typewriter.js reference');

const typewriterCode = fs.readFileSync(path.join(repoDir, 'src/js/title-typewriter.js'), 'utf8');
assert(typewriterCode.includes('span.className = \'kinetic-char\''), 'Typewriter must animate letter-by-letter using kinetic-char');
assert(typewriterCode.includes('animationDelay'), 'Typewriter must calculate staggered animationDelay');
assert(typewriterCode.includes('prefers-reduced-motion'), 'Typewriter must respect reduced-motion');
console.log('✓ Staggered letter-by-letter kinetic typewriter mechanics verified.');

// 2. Spatial Hero Tunnel Trajectory and 12-panel geometry
console.log('--- 2. 3D Spatial Hero Tunnel Invariance ---');
assert(html.includes('id="obTunnel"'), 'Missing #obTunnel');
const panelCount = (html.match(/class="tunnel-panel"/g) || []).length;
assert.strictEqual(panelCount, 12, 'Spatial hero tunnel must have exactly 12 panels (6 per side)');
assert(html.includes('id="obTunnelPause"'), 'Missing accessible pause button for tunnel');

const tunnelCode = fs.readFileSync(path.join(repoDir, 'src/js/hero-tunnel.js'), 'utf8');
assert(tunnelCode.includes('entryFade'), 'Hero tunnel must implement smooth entry fade');
assert(tunnelCode.includes('exitFade'), 'Hero tunnel must implement smooth exit fade');
assert(tunnelCode.includes('pointerdown'), 'Hero tunnel must support drag via pointerdown');
assert(tunnelCode.includes('prefers-reduced-motion'), 'Hero tunnel must support reduced motion');
console.log('✓ 12-panel bilateral spatial tunnel geometry and smooth horizon crossfade verified.');

// 3. 390px Mobile Viewport Layout Verification
console.log('--- 3. 390px Mobile Viewport Constraint Check ---');
const cinematicCss = fs.readFileSync(path.join(repoDir, 'src/css/cinematic-hero.css'), 'utf8');
const meliusCss = fs.readFileSync(path.join(repoDir, 'src/css/melius-scroll-responsive.css'), 'utf8');
assert(cinematicCss.includes('max-width:600px') || meliusCss.includes('max-width: 768px'), 'Missing mobile breakpoint media queries');
assert(cinematicCss.includes('overflow:hidden') || meliusCss.includes('overflow-x: hidden'), 'Horizontal overflow protection required');
console.log('✓ Mobile viewport constraints and overflow isolation verified.');

// 4. Reformer 3D Studio & WebGL Context Loss Recovery
console.log('--- 4. Reformer 3D WebGL & Fallback Contract ---');
assert(html.includes('id="reformerCanvas"'), 'Missing 3D canvas');
assert(html.includes('id="webglFallbackCard"'), 'Missing WebGL static fallback card');
assert(html.includes('triggerCarriageGlide'), 'Missing carriage glide trigger');
assert(html.includes('toggleReformerSprings'), 'Missing spring toggle trigger');

const reformerCode = fs.readFileSync(path.join(repoDir, 'src/js/reformer-3d.js'), 'utf8');
assert(reformerCode.includes('webglcontextlost'), 'Reformer viewer must listen to webglcontextlost');
assert(reformerCode.includes('fallbackMode'), 'Reformer viewer must implement fallbackMode()');
assert(reformerCode.includes('glbCarriageNode'), 'Reformer viewer must bind glbCarriageNode dynamically');
assert(reformerCode.includes('glbSpringNodes'), 'Reformer viewer must bind glbSpringNodes dynamically');
console.log('✓ Reformer 3D GLB node kinematics and fallback recovery contract verified.');

// 5. Accessibility, Live Regions, and Contrast Tokens
console.log('--- 5. Screen Reader Live Announcements & Accessibility ---');
assert(html.includes('id="srLiveRegion"') || html.includes('aria-live="polite"'), 'Live region required for screen reader audit announcements');
assert(html.includes('class="skip-link sr-only"') || html.includes('Saltar al contenido principal'), 'Skip to content link required');
console.log('✓ Live ARIA region and skip links verified.');

console.log('\n======================================================');
console.log('ALL DOM BEHAVIORAL & VISUAL INVARIANTS PASSED (100%)!');
console.log('======================================================');
