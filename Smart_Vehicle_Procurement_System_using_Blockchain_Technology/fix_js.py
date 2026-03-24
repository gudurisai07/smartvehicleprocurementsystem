import re

filepath = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates\seller\addVehicle.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

bad_script_pattern = r'// RTO Verification Logic.*?submitBtn\.classList\.add\(\'opacity-50\', \'cursor-not-allowed\'\); \} \} catch \(error\) \{ rtoStatus\.textContent ="Error contacting RTO API/Server\."; rtoStatus\.className ="text-xs mt-1 text-red-400"; \} \}'
good_script = """
        // RTO Verification Logic
        async function verifyVehicle() {
            const vehicle_no = document.getElementById('vehicle_number').value;
            const rtoStatus = document.getElementById('rto-status');
            const submitBtn = document.getElementById('submit-btn');
            const rtoSection = document.getElementById('rto-details-section');

            if (!vehicle_no) {
                rtoStatus.textContent = "Please enter a vehicle number.";
                rtoStatus.className = "text-xs mt-1 text-red-400";
                return;
            }

            rtoStatus.textContent = "Verifying with RTO Database...";
            rtoStatus.className = "text-xs mt-1 text-yellow-400";

            try {
                const response = await fetch(`/verify_rto_vehicle?vehicle_number=${encodeURIComponent(vehicle_no)}`);
                const data = await response.json();

                if (data.success) {
                    rtoStatus.textContent = "Verified successfully! Vehicle matches RTO records.";
                    rtoStatus.className = "text-xs mt-1 text-green-400";
                    
                    document.getElementById('rto_owner').value = data.owner_name;
                    document.getElementById('rto_model').value = data.model;
                    document.getElementById('rto_fuel').value = data.fuel;
                    
                    if(rtoSection) rtoSection.classList.remove('hidden');
                    
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                } else {
                    rtoStatus.textContent = "FAILED: " + data.message;
                    rtoStatus.className = "text-xs mt-1 text-red-500 font-semibold uppercase animate-pulse";
                    if(rtoSection) rtoSection.classList.add('hidden');
                    submitBtn.disabled = true;
                    submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
                }
            } catch (error) {
                rtoStatus.textContent = "Error contacting RTO API/Server.";
                rtoStatus.className = "text-xs mt-1 text-red-400";
            }
        }
        
        async function getLiveLocation() {
            const locStatus = document.getElementById('location-status');
            const locInput = document.getElementById('location');
            if (navigator.geolocation) {
                locStatus.textContent = "Fetching GPS coordinates...";
                locStatus.classList.remove('hidden');
                navigator.geolocation.getCurrentPosition(async (position) => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    
                    try {
                        const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
                        const data = await response.json();
                        if (data && data.display_name) {
                            locInput.value = data.display_name;
                            locStatus.textContent = "Location pinned successfully!";
                            locStatus.className = "text-xs mt-1 text-green-400";
                        } else {
                            locInput.value = `${lat}, ${lon}`;
                            locStatus.textContent = "Coordinates fetched manually.";
                        }
                    } catch {
                        locInput.value = `${lat}, ${lon}`;
                        locStatus.textContent = "Using raw coordinates.";
                    }
                }, () => {
                    locStatus.textContent = "Location access denied. Type manually.";
                    locStatus.className = "text-xs mt-1 text-red-400";
                });
            } else {
                locStatus.textContent = "Geolocation not supported by this browser.";
                locStatus.className = "text-xs mt-1 text-red-400";
            }
        }
"""

content = re.sub(bad_script_pattern, good_script, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fix applied")
