import os

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

fixed = 0
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            fp = os.path.join(root, file)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Upgrade top navbar button texts and logo text
            new_content = content.replace('glass-btn text-white py-2 px-4 rounded-full text-sm', 'glass-btn text-white py-2 px-5 rounded-full text-base font-semibold md:text-lg')
            new_content = new_content.replace('rounded-full text-sm', 'rounded-full text-base font-medium')
            
            # also text-sm -> text-base in nav buttons
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed += 1
                print(f"Upgraded nav text in: {fp}")

print(f"\nDone. Upgraded navbar text in {fixed} templates.")
