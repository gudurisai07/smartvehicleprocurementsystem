import re
import os

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

# Color palette for labels - cycling through attractive colours
LABEL_COLORS = [
    'text-indigo-400',   # indigo
    'text-cyan-400',     # cyan
    'text-purple-400',   # purple
    'text-green-400',    # green
    'text-yellow-400',   # yellow
    'text-pink-400',     # pink
    'text-blue-400',     # blue
    'text-teal-400',     # teal
    'text-orange-400',   # orange
    'text-rose-400',     # rose
]

def add_label_colors(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    color_idx = [0]  # use list to allow mutation inside lambda
    
    def replace_label(match):
        full = match.group(0)
        color = LABEL_COLORS[color_idx[0] % len(LABEL_COLORS)]
        color_idx[0] += 1
        # Replace text-gray-300 or text-gray-400 in label
        return re.sub(r'text-gray-[0-9]{3}', color, full, count=1)
    
    # Match <label ...class="..."> elements
    content = re.sub(r'<label\s[^>]*class="[^"]*text-gray-[0-9]{3}[^"]*"[^>]*>', replace_label, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

count = 0
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            add_label_colors(os.path.join(root, file))
            count += 1

print(f"Colorful labels applied to {count} templates.")
