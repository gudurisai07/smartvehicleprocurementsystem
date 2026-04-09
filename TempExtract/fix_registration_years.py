import os
import django
import random
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Vehicle_Procurement_System_using_Blockchain_Technology.settings')
django.setup()

from seller.models import RTODatabase

records = RTODatabase.objects.all()
count = 0

for r in records:
    vn = r.vehicle_number
    # Extract district code (e.g., AP39 -> 39)
    try:
        dist_str = ""
        for char in vn:
            if char.isdigit():
                dist_str += char
            elif dist_str:
                break
        dist_code = int(dist_str)
    except:
        dist_code = 1

    # Logic for 2011-2024 mapping:
    if dist_code <= 15:
        s, e = 2011, 2014
    elif dist_code <= 30:
        s, e = 2014, 2018
    elif dist_code <= 40:
        s, e = 2018, 2021
    else:
        s, e = 2021, 2024

    start_date = datetime.date(s, 1, 1)
    end_date = datetime.date(e, 12, 31)
    days = (end_date - start_date).days
    r.registration_date = start_date + datetime.timedelta(days=random.randrange(days))
    r.save()
    count += 1

print(f"Successfully updated {count} records with series-appropriate years (2011-2024).")
