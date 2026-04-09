import os
import django
import sys
import random
from datetime import date, timedelta

sys.path.insert(0, r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Vehicle_Procurement_System_using_Blockchain_Technology.settings')
django.setup()

from seller.models import RTODatabase

# Force-update ALL records with realistic historical dates 2005-2024
start = date(2005, 1, 1)
range_days = (date(2024, 12, 31) - start).days

records = list(RTODatabase.objects.all())
for r in records:
    r.registration_date = start + timedelta(days=random.randint(0, range_days))

RTODatabase.objects.bulk_update(records, ['registration_date'], batch_size=100)
print(f"Updated all {len(records)} vehicles with historical registration dates (2005-2024).")
