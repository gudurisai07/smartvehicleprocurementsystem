import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

# Label colors cycling list
COLORS = [
    'text-indigo-400', 'text-cyan-400', 'text-purple-400',
    'text-green-400', 'text-yellow-400', 'text-pink-400',
    'text-blue-400', 'text-teal-400', 'text-orange-400', 'text-rose-400',
]

def upgrade_labels(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    color_idx = [0]

    def apply_color(match):
        full = match.group(0)
        color = COLORS[color_idx[0] % len(COLORS)]
        color_idx[0] += 1
        # Change text-xs to text-sm if found, and update text-gray colors
        full = re.sub(r'\btext-xs\b', 'text-sm', full)
        full = re.sub(r'\btext-gray-[0-9]{3}\b', color, full, count=1)
        return full

    # Match label tags
    content = re.sub(r'<label\s[^>]*>', apply_color, content)

    # Also: any text-xs label-like elements to text-sm 
    # Global background consistency: ensure bg-gray-900 body
    content = content.replace('<body class="bg-gray-900 font-sans relative text-white">', 
                               '<body class="font-sans relative text-white" style="background: linear-gradient(-45deg, #0a0a1a, #0f172a, #0d1b2a, #0a0a1a); background-size: 400% 400%; animation: gradientShift 20s ease infinite; min-height: 100vh;">')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Add gradientShift animation to pages that don't have it
def add_gradient_anim(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if 'gradientShift' not in content and '<style>' in content:
        gradient_css = """
  @keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }"""
        content = content.replace('<style>', '<style>' + gradient_css)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

count = 0
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            fp = os.path.join(root, file)
            upgrade_labels(fp)
            add_gradient_anim(fp)
            count += 1

print(f"Upgraded labels and background animation in {count} templates.")
