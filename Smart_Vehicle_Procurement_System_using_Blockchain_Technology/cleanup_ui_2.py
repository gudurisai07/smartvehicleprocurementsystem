import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

def deep_clean_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Three.js canvas and script imports
    content = re.sub(r'<canvas\s+id="three-canvas"\s*>\s*</canvas>', '', content)
    content = re.sub(r'<script\s+src="https://cdnjs\.cloudflare\.com/ajax/libs/three\.js[^>]+></script>', '', content)
    
    # 2. Remove the Three.js setup script block entirely
    content = re.sub(r'<script>\s*// Three.js Setup.*?</script>', '', content, flags=re.DOTALL)
    
    # 3. Replace 'glass-effect' with 'bg-gray-800' for a solid clean look
    content = content.replace('glass-effect', 'bg-gray-800')
    
    # 4. Remove empty CSS blocks left behind in earlier script
    content = re.sub(r'\.\s*\{\s*\}', '', content)
    
    # 5. Clean up leftover class=" " spacing
    content = re.sub(r'class="\s+', 'class="', content)
    content = re.sub(r'\s{2,}"', '"', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            deep_clean_html(os.path.join(root, file))

print("Deep clean for Three.js and glass-effects completed.")
