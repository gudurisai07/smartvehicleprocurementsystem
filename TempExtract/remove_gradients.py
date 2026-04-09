import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

def remove_gradients_only(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Remove animated gradient CSS classes - bg-gradient-to-* from-* to-*
    # But ONLY from background elements, NOT from text or buttons
    
    # 1. Remove animated gradient-x from section/div backgrounds
    content = re.sub(r'\bbg-gradient-to-r\b[\s]+\bfrom-[a-z]+-[0-9]+\b[\s]+\bto-[a-z]+-[0-9]+\b', 'bg-gray-900', content)
    content = re.sub(r'\bbg-gradient-to-b\b[\s]+\bfrom-[a-z]+-[0-9]+\b[\s]+\bto-[a-z]+-[0-9]+\b', 'bg-gray-900', content)
    content = re.sub(r'\bbg-gradient-to-br\b[\s]+\bfrom-[a-z]+-[0-9]+\b[\s]+\bto-[a-z]+-[0-9]+\b', 'bg-gray-900', content)

    # 2. Remove hero/section background images (heavy background)
    # Only remove the CSS for background images in <style> blocks
    content = re.sub(r'background:\s*url\([^)]+\)\s*no-repeat.*?;', 'background: #111827;', content)
    content = re.sub(r'background-attachment:\s*fixed;', '', content)
    
    # 3. Remove the section-bg overlay class from <style> blocks
    content = re.sub(r'\.hero-bg\s*\{[^}]+\}', '.hero-bg { background: #0f172a; }', content)
    content = re.sub(r'\.section-bg\s*\{[^}]+\}', '.section-bg { background: #1e293b; }', content)
    content = re.sub(r'\.overlay\s*\{[^}]+\}', '', content)
    
    # 4. Clean up multiple spaces
    content = re.sub(r'  +', ' ', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

count = 0
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            remove_gradients_only(os.path.join(root, file))
            count += 1

print(f"Done! Removed heavy background gradients from {count} files.")
