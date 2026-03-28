import re
import os

base_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"
files_to_update = [
    "userLoginForm.html",
    "userRegisterForm.html",
    "buyerLoginForm.html",
    "buyerRegisterForm.html",
    "sellerLoginForm.html",
    "sellerRegisterForm.html",
    "adminLoginForm.html"
]

new_navbar_html = """
  <!-- Minimal Navbar -->
  <nav class="glass-nav py-4 px-6 flex justify-between items-center relative z-20">
    <a href="/" class="flex items-center space-x-2 text-white font-bold text-xl">
      <img src="https://img.icons8.com/fluency/48/ffffff/sports-car.png" class="w-8 h-8">
      <span>SmartVehicle</span>
    </a>
    
    <!-- Desktop Menu -->
    <div class="hidden md:flex space-x-3">
      <a href="/" class="glass-btn text-white py-2 px-5 rounded-full text-base font-semibold">Home</a>
      <a href="userLoginForm" class="glass-btn text-indigo-300 py-2 px-5 rounded-full text-base font-semibold">Login</a>
      <a href="userRegisterForm" class="glass-btn text-green-300 py-2 px-4 rounded-full text-base font-medium">Register</a>
      <a href="adminHome" class="glass-btn text-gray-300 py-2 px-5 rounded-full text-base font-semibold">Admin</a>
    </div>

    <!-- Mobile Menu Button (Three Dots) -->
    <button id="mobileMenuBtn" class="md:hidden text-white text-3xl focus:outline-none p-2 glass-btn rounded-full w-12 h-12 flex items-center justify-center">
      ⋮
    </button>
  </nav>

  <!-- Mobile Dropdown Menu -->
  <div id="mobileMenu" class="absolute top-20 right-4 rounded-xl z-50 hidden flex-col w-48 overflow-hidden shadow-2xl glass-nav border border-gray-600">
    <a href="/" class="block px-6 py-4 text-white hover:bg-gray-800 font-medium border-b border-gray-700">🏠 Home</a>
    <a href="userLoginForm" class="block px-6 py-4 text-indigo-300 hover:bg-gray-800 font-medium border-b border-gray-700">🔑 Login</a>
    <a href="userRegisterForm" class="block px-6 py-4 text-green-300 hover:bg-gray-800 font-medium border-b border-gray-700">📝 Register</a>
    <a href="adminHome" class="block px-6 py-4 text-gray-300 hover:bg-gray-800 font-medium">🛡️ Admin</a>
  </div>

  <script>
    document.getElementById('mobileMenuBtn').addEventListener('click', function() {
      const menu = document.getElementById('mobileMenu');
      if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        menu.classList.add('flex');
        menu.style.animation = 'fadeSlideIn 0.3s ease-out forwards';
      } else {
        menu.classList.add('hidden');
        menu.classList.remove('flex');
      }
    });
  </script>
"""

for fname in files_to_update:
    fpath = os.path.join(base_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to match the old nav block
        # It typically starts with <nav ...> and ends with </nav>
        nav_pattern = re.compile(r'<!-- Minimal Navbar -->\s*<nav[^>]*>.*?</nav>', re.DOTALL)
        
        if nav_pattern.search(content):
            content = nav_pattern.sub(new_navbar_html.strip(), content, count=1)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Updated", fname)
        else:
            print("Nav block not found exactly in", fname, ", trying loose match...")
            loose_pattern = re.compile(r'<nav[^>]*>.*?</nav>', re.DOTALL)
            if loose_pattern.search(content):
                 # Assuming first nav is the top nav
                 content = loose_pattern.sub(new_navbar_html.strip(), content, count=1)
                 with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                 print("Updated loosely", fname)
            else:
                 print("Not found in", fname)
