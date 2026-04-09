import os
import django
import sys

sys.path.insert(0, r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Vehicle_Procurement_System_using_Blockchain_Technology.settings')
django.setup()

from seller.models import RTODatabase

# Seed 50 Andhra Pradesh vehicles with realistic data
vehicles = [
    # Format: vehicle_number, owner_name, vehicle_model, fuel_type
    ("AP39FP5532", "Ravi Kumar", "Toyota Innova", "Diesel"),
    ("AP34DH5001", "Suresh Reddy", "Maruti Swift", "Petrol"),
    ("AP39AB1234", "Ramesh Naidu", "Maruti Swift", "Petrol"),
    ("AP28CD7890", "Priya Sharma", "Honda City", "Petrol"),
    ("AP09XY3456", "Venkat Rao", "Hyundai Creta", "Petrol"),
    ("AP16FG2345", "Lakshmi Devi", "Toyota Fortuner", "Diesel"),
    ("AP05HJ6789", "Srinivas Reddy", "Mahindra Scorpio", "Diesel"),
    ("AP21KL4567", "Anjali Krishnan", "Tata Nexon", "Petrol"),
    ("AP30MN8901", "Rajesh Kumar", "Hyundai i20", "Petrol"),
    ("AP11PQ2345", "Padma Rao", "Honda Amaze", "Petrol"),
    ("AP22RS6789", "Govind Swamy", "Maruti Baleno", "Petrol"),
    ("AP33TU0123", "Meena Kumari", "Kia Seltos", "Petrol"),
    ("AP44VW4567", "Nagaraju", "MG Hector", "Diesel"),
    ("AP55XY8901", "Kavitha Reddy", "Ford EcoSport", "Petrol"),
    ("AP01ZA2345", "Ramana Murthy", "Renault Kwid", "Petrol"),
    ("AP02BC6789", "Sunitha Devi", "Maruti Alto", "Petrol"),
    ("AP03DE0123", "Venkateswara Rao", "Tata Tiago", "Petrol"),
    ("AP04FG4567", "Sai Krishna", "Hyundai Venue", "Petrol"),
    ("AP06HI8901", "Durga Prasad", "Mahindra Thar", "Diesel"),
    ("AP07JK2345", "Ramya Sri", "Toyota Camry", "Petrol"),
    ("AP08LM6789", "Anil Babu", "BMW 3 Series", "Petrol"),
    ("AP10NO0123", "Swetha Goud", "Mercedes A-Class", "Petrol"),
    ("AP12PQ4567", "Bhaskar Reddy", "Audi A4", "Petrol"),
    ("AP13RS8901", "Chandra Kala", "Volkswagen Polo", "Petrol"),
    ("AP14TU2345", "Mohan Das", "Skoda Rapid", "Diesel"),
    ("AP15VW6789", "Nirmala Devi", "Tata Harrier", "Diesel"),
    ("AP17XY0123", "Kishore Kumar", "Jeep Compass", "Diesel"),
    ("AP18ZA4567", "Radha Krishna", "Mahindra XUV700", "Diesel"),
    ("AP19BC8901", "Satyam Babu", "Hyundai Tucson", "Diesel"),
    ("AP20DE2345", "Usha Rani", "Kia Carnival", "Diesel"),
    ("AP23FG6789", "Prasad Kumar", "Toyota Fortuner", "Diesel"),
    ("AP24HI0123", "Indira Devi", "Maruti Dzire", "Petrol"),
    ("AP25JK4567", "Venkata Krishna", "Renault Duster", "Diesel"),
    ("AP26LM8901", "Bhavani Devi", "Nissan Magnite", "Petrol"),
    ("AP27NO2345", "Srinivasa Rao", "Ford Ecosport", "Diesel"),
    ("AP29PQ6789", "Saritha Devi", "Honda WRV", "Petrol"),
    ("AP31RS0123", "Raju Naik", "Tata Safari", "Diesel"),
    ("AP32TU4567", "Madhavi Latha", "Maruti Ertiga", "CNG"),
    ("AP35VW8901", "Suryanarayana", "Toyota Etios", "Petrol"),
    ("AP36XY2345", "Parvathi Devi", "Datsun GO", "Petrol"),
    ("AP37ZA6789", "Ashok Kumar", "Hyundai Santro", "Petrol"),
    ("AP38BC0123", "Nandini Reddy", "Maruti Wagon R", "CNG"),
    ("AP40DE4567", "Balakrishna", "Mahindra Bolero", "Diesel"),
    ("AP41FG8901", "Sridevi", "Tata Punch", "Petrol"),
    ("AP42HI2345", "Rameshu", "Maruti S-Presso", "Petrol"),
    ("AP43JK6789", "Tulasi Devi", "Honda Jazz", "Petrol"),
    ("AP45LM0123", "Prakash Rao", "Hundai Xcent", "Diesel"),
    ("AP46NO4567", "Kumari Devi", "Tata Altroz", "Petrol"),
    ("AP47PQ8901", "Vamshi Krishna", "Toyota Yaris", "Petrol"),
    ("AP48RS2345", "Shalini Rao", "Maruti Ciaz", "Petrol"),
]

created = 0
skipped = 0
for veh_no, owner, model, fuel in vehicles:
    obj, is_new = RTODatabase.objects.get_or_create(
        vehicle_number=veh_no,
        defaults={
            'owner_name': owner,
            'vehicle_model': model,
            'fuel_type': fuel
        }
    )
    if is_new:
        created += 1
    else:
        skipped += 1

print(f"Done! Added {created} new vehicles, {skipped} already existed.")
print(f"Total vehicles in RTO DB: {RTODatabase.objects.count()}")

