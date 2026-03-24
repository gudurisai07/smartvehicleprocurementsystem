import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

def clean_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove standard animation classes
    animation_classes = [
        r'\banimate-pulseGlow\b',
        r'\banimate-spin\b',
        r'\banimate-slideIn\b',
        r'\banimate-fadeIn\b',
        r'\banimate-gradient-x\b',
        r'\banimate-pulse\b',
        r'\banimate-bounce\b',
        r'\bcard-hover\b'
    ]
    for cls in animation_classes:
        content = re.sub(cls, '', content)

    # 2. Remove inline animation-delay styles
    content = re.sub(r'style="animation-delay:\s*[0-9.]+s;?"', '', content)
    
    # 3. Clean up borders (Tailwind)
    border_classes = [
        r'\bborder\b',
        r'\bborder-white/10\b',
        r'\bborder-white/20\b',
        r'\bborder-gray-[0-9]+\b',
        r'\bborder-indigo-[0-9]+\b',
        r'\bborder-purple-[0-9]+\b',
        r'\bborder-t\b', r'\bborder-b\b', r'\bborder-l\b', r'\bborder-r\b'
    ]
    for cls in border_classes:
        content = re.sub(cls, '', content)
        
    # 4. Remove CSS block styling for glass-effect borders / animations
    content = re.sub(r'border:\s*1px\s*solid\s*rgba[^;]+;', '', content)
    content = re.sub(r'animation:\s*[^;]+;', '', content)
    
    # 5. Clean up multiple spaces inside class attributes caused by removals
    content = re.sub(r'class="\s+', 'class="', content)
    content = re.sub(r'\s+"', '"', content)
    content = re.sub(r'\s{2,}', ' ', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            clean_html_file(os.path.join(root, file))

print("Cleanup script completed successfully.")
