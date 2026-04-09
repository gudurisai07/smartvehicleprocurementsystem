import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Vehicle_Procurement_System_using_Blockchain_Technology.settings')
django.setup()

from Buyers.models import userRegisteredTable
from seller.models import sellerRegisteredTable

print("--- Buyers ---")
for u in userRegisteredTable.objects.all():
    print(f"ID: {u.id} | Login: {u.loginid} | Email: {u.email} | Mobile: '{u.mobile}'")

print("\n--- Sellers ---")
for s in sellerRegisteredTable.objects.all():
    print(f"ID: {s.id} | Login: {s.loginid} | Email: {s.email} | Mobile: '{s.mobile}'")
