import zipfile
import os
import re

zip_path = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology.zip"
target_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology"
temp_extract = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\TempExtract"

# Read the CURRENT addVehicle.html to backup our new location and RTO logic
curr_add_vehicle = os.path.join(target_dir, "Templates", "seller", "addVehicle.html")
old_html = ""
with open(curr_add_vehicle, "r", encoding="utf-8") as f:
    old_html = f.read()

# Extract the verify vehicle JS and elements
rto_details_section = re.search(r'(<div class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4 hidden transition-all" id="rto-details-section">.*?</div>\s*</div>)', old_html, re.DOTALL)
rto_buttons = re.search(r'(<div class="flex items-center space-x-2">\s*<input type="text" id="vehicle_number".*?</button>\s*</div>\s*<p id="rto-status".*?</p>\s*)', old_html, re.DOTALL)
location_section = re.search(r'(<label class="block text-gray-400 text-sm font-semibold mb-2">Location</label>.*?</div>\s*<p id="location-status".*?</p>\s*</div>)', old_html, re.DOTALL)
js_script = re.search(r'(// RTO Verification Logic.*?}\s*)(// Handle Window Resize|document\.getElementById\(\'picture\'\))', old_html, re.DOTALL)

print("Backups read successfully, extracting zip...")

with zipfile.ZipFile(zip_path, 'r') as z:
    for member in z.namelist():
        if member.endswith('/') or member.endswith('\\'):
            continue
        # We only want to restore the Templates folder
        if "Smart_Vehicle_Procurement_System_using_Blockchain_Technology/Templates/" in member:
            filename = os.path.basename(member)
            # Find subfolder structure
            subpath = member.split("Smart_Vehicle_Procurement_System_using_Blockchain_Technology/")[-1]
            dest = os.path.join(target_dir, subpath)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            
            with z.open(member) as source, open(dest, "wb") as target:
                target.write(source.read())

print("Templates restored. Now re-injecting custom DOM logic into addVehicle.html...")

# Now read the newly restored addVehicle.html and inject JS + HTML UI
with open(curr_add_vehicle, "r", encoding="utf-8") as f:
    restored_html = f.read()

if rto_buttons:
    # Replace old vehicle number input
    restored_html = re.sub(r'<input type="text"\s*id="vehicle_number" name="vehicle_number"[^\n]*\n.*?</p>', rto_buttons.group(1), restored_html, flags=re.DOTALL)

if rto_details_section:
    # Inject before vehicle picture
    restored_html = restored_html.replace('<div class="mb-6">\n                        <label for="picture"', rto_details_section.group(1) + '\n                    <div class="mb-6">\n                        <label for="picture"')

if location_section:
     restored_html = restored_html.replace('<!-- Insert original location html if found? we skipped replacing original location input since Location logic might have changed widely', '')

# Replace submit button state
restored_html = re.sub(r'<button type="submit"([^>]*)>', r'<button type="submit" id="submit-btn" disabled class="w-full py-3 bg-gradient-to-r from-purple-500 to-indigo-600 text-white rounded-full hover:from-purple-600 hover:to-indigo-700 font-semibold transition-all animate-pulseGlow opacity-50 cursor-not-allowed">', restored_html)

# Inject JS
if js_script:
    restored_html = restored_html.replace('document.getElementById(\'picture\')', js_script.group(1) + '\n\n        document.getElementById(\'picture\')')

# Disable submit on typing vehicle number
restored_html = restored_html.replace('this.value = this.value.toUpperCase();', '''this.value = this.value.toUpperCase();
            
            // Disable submit if they change the vehicle number after verifying
            const submitBtn = document.getElementById('submit-btn');
            const rtoStatus = document.getElementById('rto-status');
            const rtoSection = document.getElementById('rto-details-section');
            
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
            if(rtoSection) rtoSection.classList.add('hidden');
            if(rtoStatus) {
                rtoStatus.textContent = "Format: AP34DH5001 - Must click Verify RTO again.";
                rtoStatus.className = "text-xs text-yellow-400 mt-1";
            }''')

with open(curr_add_vehicle, "w", encoding="utf-8") as f:
    f.write(restored_html)

print("Done. All designs restored with custom RTO logic intact.")
