from pathlib import Path

p = Path('/home/user/openbreak/templates/part4_js_logic.html')
content = p.read_text(encoding='utf-8')

old_code = """    function toggleFaq(btn) {
      const item = btn.parentElement;
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => {
        i.classList.remove('open');
        const trigger = i.querySelector('.faq-trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    }"""

new_code = """    function toggleFaq(btn) {
      const item = btn.parentElement;
      const isOpen = item.classList.contains('is-open') || item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => {
        i.classList.remove('is-open');
        i.classList.remove('open');
        const trigger = i.querySelector('.faq-trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        item.classList.add('is-open');
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    }"""

assert old_code in content, "old_code not found in part4_js_logic.html"
content = content.replace(old_code, new_code)
p.write_text(content, encoding='utf-8')
print("Successfully synced FAQ toggle class list in part4_js_logic.html")
