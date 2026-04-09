import re
import os

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

# 1. Fix login page - add animated gradient background
login_file = os.path.join(template_dir, "userLoginForm.html")
with open(login_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Add animated gradient CSS to style block
animated_bg_css = """
  @keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  .animated-bg {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0f172a, #1a1a2e);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
  }
"""

content = content.replace('</style>', animated_bg_css + '\n</style>')
content = content.replace('<body class="bg-gray-900', '<body class="animated-bg')
content = content.replace('<body class="bg-gray-900 font-sans relative text-white">', '<body class="animated-bg font-sans relative text-white min-h-screen">')

with open(login_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Login page animated bg done.")

# 2. Apply glass transparent buttons across all pages
def apply_glass_buttons(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Add glass button CSS to any style block
    glass_btn_css = """
  .glass-btn {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    transition: all 0.3s ease;
  }
  .glass-btn:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
  }
"""
    if '<style>' in content and 'glass-btn' not in content:
        content = content.replace('</style>', glass_btn_css + '</style>')
        
    # Replace nav-button solid gray backgrounds with glass
    content = re.sub(
        r'class="nav-button bg-gray-[0-9]{3} text-white py-2 px-6 rounded-full (hover:[^\s"]+\s?)*"',
        'class="nav-button glass-btn text-white py-2 px-6 rounded-full"',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            apply_glass_buttons(os.path.join(root, file))

print("Glass buttons applied to all pages.")
