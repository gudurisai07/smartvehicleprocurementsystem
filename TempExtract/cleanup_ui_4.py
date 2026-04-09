import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

def patch_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix leftover weird tailwind classes
    content = re.sub(r'bg-gray-[0-9]{3}\s+to-[a-z]+-[0-9]{3}', 'text-blue-400', content)
    content = re.sub(r'hover:hover:to-[a-z]+-[0-9]{3}', 'hover:bg-gray-700', content)
    content = content.replace('hover:hover:transition', 'hover:bg-gray-700 transition')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            patch_html(os.path.join(root, file))

print("Patch applied.")
