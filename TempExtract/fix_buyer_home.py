import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

fixed = 0
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            fp = os.path.join(root, file)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            new_content = content.replace('href="buyerHome"', 'href="userHome"')
            new_content = new_content.replace("href='buyerHome'", "href='userHome'")
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed += 1
                print(f"Fixed: {fp}")

print(f"\nDone. Fixed buyerHome links in {fixed} files.")
