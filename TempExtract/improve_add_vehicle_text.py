import os
import re

fp = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates\seller\addVehicle.html"

with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()

# Make labels larger (text-sm -> text-base or text-lg)
content = content.replace('text-sm font-semibold', 'text-base font-semibold')

# Make inputs a bit larger if they are text-sm
content = content.replace('text-sm cursor-not-allowed', 'text-base cursor-not-allowed')
content = content.replace('text-xs text-gray-400', 'text-sm text-gray-400')

with open(fp, 'w', encoding='utf-8') as f:
    f.write(content)

print("Improved text sizes in addVehicle.html")
