import re

filepath = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace navbar links - remove all legacy buyer/seller login/register
# Replace old nav block
old_nav = re.search(r'<div class="space-x-6">.*?</div>', content, re.DOTALL)
if old_nav:
    print("Found nav block:", old_nav.group()[:200])

# Replace all old nav links with unified ones
content = re.sub(
    r'<div class="space-x-6">.*?</div>',
    '''<div class="space-x-6">
  <a href="/" class="nav-button bg-gray-900 text-white py-2 px-6 rounded-full hover:bg-gray-700 transition">Home</a>
  <a href="userLoginForm" class="nav-button bg-indigo-600 text-white py-2 px-6 rounded-full hover:bg-indigo-500 transition">Login</a>
  <a href="userRegisterForm" class="nav-button bg-green-600 text-white py-2 px-6 rounded-full hover:bg-green-500 transition">Register</a>
  <a href="adminLoginForm" class="nav-button bg-gray-700 text-white py-2 px-6 rounded-full hover:bg-gray-600 transition">Admin</a>
 </div>''',
    content, count=1, flags=re.DOTALL
)

# Fix hero heading which was broken (had bg-clip-text text-transparent bg-gray-900 that makes it invisible)
content = content.replace(
    'bg-clip-text text-transparent bg-gray-900',
    'text-white'
)

# Replace "Discover More" link with proper Register/Login CTAs
content = re.sub(
    r'<a href="#features"[^>]*>Discover More</a>',
    '<a href="userRegisterForm" class="inline-block bg-green-600 text-white py-4 px-8 rounded-full hover:bg-green-500 transition text-lg font-semibold mr-4">Get Started</a>\n  <a href="userLoginForm" class="inline-block bg-indigo-600 text-white py-4 px-8 rounded-full hover:bg-indigo-500 transition text-lg font-semibold">Login</a>',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully!")
