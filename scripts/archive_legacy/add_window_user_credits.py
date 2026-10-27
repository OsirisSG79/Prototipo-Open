from pathlib import Path

p = Path('/home/user/openbreak/src/js/demo-store.js')
content = p.read_text(encoding='utf-8')

old_end = """  // Instantiate singleton with opening balance of 8
  const storeInstance = new DemoStore(8);
  if (typeof window !== 'undefined') {
    window.OpenBreakStore = storeInstance;
    window.credits = storeInstance.credits;
  }"""

new_end = """  // Instantiate singleton with opening balance of 8
  const storeInstance = new DemoStore(8);
  if (typeof window !== 'undefined') {
    window.OpenBreakStore = storeInstance;
    window.credits = storeInstance.credits;
    window.userCredits = storeInstance.credits;
  }"""

assert old_end in content
content = content.replace(old_end, new_end)
p.write_text(content, encoding='utf-8')
print("Exposed window.userCredits in demo-store.js!")
