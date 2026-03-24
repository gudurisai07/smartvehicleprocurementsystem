import re
import os

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

new_navbar = '''<div class="space-x-6">
  <a href="/" class="nav-button bg-gray-900 text-white py-2 px-6 rounded-full hover:bg-gray-700 transition">Home</a>
  <a href="userLoginForm" class="nav-button bg-indigo-600 text-white py-2 px-6 rounded-full hover:bg-indigo-500 transition">Login</a>
  <a href="userRegisterForm" class="nav-button bg-green-600 text-white py-2 px-6 rounded-full hover:bg-green-500 transition">Register</a>
 </div>'''

def fix_auth_navbars(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Only update pages that still have the old separate login links
    if 'buyerLoginForm' in content or 'sellerLoginForm' in content:
        content = re.sub(
            r'<div class="space-x-6">.*?</div>',
            new_navbar,
            content, count=1, flags=re.DOTALL
        )
        print(f"Fixed navbar in: {os.path.basename(filepath)}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            fix_auth_navbars(os.path.join(root, file))

print("All auth navbars unified.")
