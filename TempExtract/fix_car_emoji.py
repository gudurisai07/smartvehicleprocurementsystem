import os
import re

base_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

for root, dirs, files in os.walk(base_dir):
    for fname in files:
        if fname.endswith(".html"):
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace the broken image with a car emoji
            new_content = content.replace(
                '<img src="https://img.icons8.com/fluency/48/ffffff/sports-car.png" class="w-8 h-8">',
                '<span class="text-3xl">🚗</span>'
            )
            
            if new_content != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {fpath}")
