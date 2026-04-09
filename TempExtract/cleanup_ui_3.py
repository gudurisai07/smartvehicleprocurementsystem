import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

def super_clean_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove background image classes from HTML
    content = content.replace('hero-bg', 'bg-gray-900')
    content = content.replace('section-bg', 'bg-gray-800')
    content = content.replace('overlay', '')
    
    # 2. Clear out the leftover <style> block entirely to ensure no custom borders/backgrounds remain
    content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
    
    # 3. Clean up generic Tailwind moving gradients
    content = re.sub(r'bg-gradient-to-[a-z]+\s+', 'bg-gray-800 ', content)
    content = re.sub(r'from-[a-z]+-[0-9]+\s+', '', content)
    content = re.sub(r'to-[a-z]+-[0-9]+\s+', '', content)
    content = re.sub(r'hover:from-[a-z]+-[0-9]+\s+', '', content)
    content = re.sub(r'hover:to-[a-z]+-[0-9]+\s+', 'hover:bg-gray-700 ', content)
    
    # Text gradients (titles) mapped to flat distinct colours
    content = re.sub(r'bg-clip-text text-transparent\s+', '', content)
    
    # Primary Buttons standardisation 
    content = content.replace('bg-gray-800 text-white py-4 px-8 rounded-full hover:bg-gray-700 transition text-lg font-semibold', 'bg-indigo-600 text-white py-4 px-8 rounded-lg shadow-md hover:bg-indigo-500 transition text-lg font-semibold')
    content = content.replace('bg-gray-800 text-white py-2 px-6 rounded-full hover:bg-gray-700', 'bg-indigo-600 text-white py-2 px-6 rounded-lg shadow-md hover:bg-indigo-500 transition')
    
    # Clean up double classes
    content = re.sub(r'\s{2,}', ' ', content)
    content = content.replace('class=" "', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            super_clean_html(os.path.join(root, file))

print("Super clean UI script executed.")
