import os
import django
import sys
import random

sys.path.insert(0, r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Vehicle_Procurement_System_using_Blockchain_Technology.settings')
django.setup()

from seller.models import RTODatabase

# ------- Data pools -------
AP_DISTRICT_CODES = [
    "AP01","AP02","AP03","AP04","AP05","AP06","AP07","AP08","AP09","AP10",
    "AP11","AP12","AP13","AP14","AP15","AP16","AP17","AP18","AP19","AP20",
    "AP21","AP22","AP23","AP24","AP25","AP26","AP27","AP28","AP29","AP30",
    "AP31","AP32","AP33","AP34","AP35","AP36","AP37","AP38","AP39","AP40",
    "AP41","AP42","AP43","AP44","AP45","AP46","AP47","AP48","AP49","AP50",
]

LETTER_PAIRS = [
    "AA","AB","AC","AD","AE","AF","AG","AH","AJ","AK","AL","AM","AN","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ",
    "BA","BB","BC","BD","BE","BF","BG","BH","BJ","BK","BL","BM","BN","BP","BQ","BR","BS","BT","BU","BV","BW","BX","BY","BZ",
    "CA","CB","CC","CD","CE","CF","CG","CH","CJ","CK","CL","CM","CN","CP","DA","DB","DC","DE","DF","DG","DH","DJ","DK","DL",
    "EA","EB","EC","ED","EF","EG","EH","EJ","EK","EL","FA","FB","FC","FD","FE","FF","FG","FH","FJ","FK","FL","FM","FN","FP",
    "GA","GB","GC","GD","GE","GF","GG","GH","GJ","GK","GL","GM","HH","HJ","HK","HL","HM","HN","HP","HQ","HR","HS","HT","HU",
    "JA","JB","JC","JD","JE","JF","JG","JH","JJ","JK","JL","KA","KB","KC","KD","KE","KF","KG","KH","KJ","KK","KL","KM","KN",
    "LA","LB","LC","LD","LE","LF","LG","LH","MA","MB","MC","MD","ME","MF","MG","MH","MJ","MK","ML","MN","MP",
    "NA","NB","NC","ND","NE","NF","NG","NH","NJ","NK","NL","NM","PA","PB","PC","PD","PE","PF","PG","PH","PJ","PK","PL",
    "RA","RB","RC","RD","RE","RF","RG","RH","RJ","RK","RL","RM","SA","SB","SC","SD","SE","SF","SG","SH","SJ","SK","SL","SM",
    "TA","TB","TC","TD","TE","TF","TG","TH","TJ","TK","TL","UA","UB","UC","VA","VB","VC","VD","VE","VF","VG","VH","VJ","VK",
    "WA","WB","WC","XA","XB","XC","XD","XE","XF","XG","XH","XJ","XK","XL","XM","XN","XP","XQ","XR","XS","XT","XU","XV","XY","XZ",
    "YA","YB","YC","YD","YE","YF","ZA","ZB","ZC","ZD","ZE","ZF","ZG","ZH","ZJ","ZK","ZL",
]

MODELS = [
    ("Maruti Swift", "Petrol"), ("Maruti Baleno", "Petrol"), ("Maruti Dzire", "Petrol"),
    ("Maruti Alto K10", "Petrol"), ("Maruti Wagon R", "CNG"), ("Maruti Ertiga", "Petrol"),
    ("Maruti S-Presso", "Petrol"), ("Maruti Ciaz", "Petrol"), ("Maruti Brezza", "Petrol"),
    ("Hyundai i20", "Petrol"), ("Hyundai Creta", "Petrol"), ("Hyundai Venue", "Petrol"),
    ("Hyundai Santro", "Petrol"), ("Hyundai Xcent", "Diesel"), ("Hyundai Tucson", "Diesel"),
    ("Hyundai Verna", "Petrol"), ("Hyundai Grand i10", "Petrol"),
    ("Toyota Innova", "Diesel"), ("Toyota Fortuner", "Diesel"), ("Toyota Camry", "Petrol"),
    ("Toyota Etios", "Petrol"), ("Toyota Yaris", "Petrol"), ("Toyota Glanza", "Petrol"),
    ("Honda City", "Petrol"), ("Honda Amaze", "Petrol"), ("Honda Jazz", "Petrol"),
    ("Honda WRV", "Petrol"), ("Honda Elevate", "Petrol"),
    ("Tata Nexon", "Petrol"), ("Tata Harrier", "Diesel"), ("Tata Safari", "Diesel"),
    ("Tata Tiago", "Petrol"), ("Tata Altroz", "Petrol"), ("Tata Punch", "Petrol"),
    ("Mahindra Scorpio", "Diesel"), ("Mahindra Bolero", "Diesel"), ("Mahindra Thar", "Diesel"),
    ("Mahindra XUV700", "Diesel"), ("Mahindra XUV300", "Diesel"),
    ("Kia Seltos", "Petrol"), ("Kia Carnival", "Diesel"), ("Kia Sonet", "Diesel"),
    ("MG Hector", "Diesel"), ("MG Astor", "Petrol"),
    ("Ford EcoSport", "Petrol"), ("Ford Endeavour", "Diesel"),
    ("Renault Kwid", "Petrol"), ("Renault Duster", "Diesel"), ("Renault Triber", "Petrol"),
    ("Volkswagen Polo", "Petrol"), ("Volkswagen Taigun", "Petrol"),
    ("Skoda Rapid", "Diesel"), ("Skoda Kushaq", "Petrol"),
    ("Jeep Compass", "Diesel"), ("Jeep Meridian", "Diesel"),
    ("BMW 3 Series", "Petrol"), ("BMW 5 Series", "Diesel"),
    ("Mercedes C-Class", "Petrol"), ("Mercedes E-Class", "Diesel"),
    ("Audi A4", "Petrol"), ("Audi Q5", "Diesel"),
    ("Nissan Magnite", "Petrol"), ("Datsun GO", "Petrol"),
    ("Bajaj Pulsar 150", "Petrol"), ("Hero Splendor", "Petrol"),
    ("Royal Enfield Classic 350", "Petrol"),
]

NAMES = [
    "Ravi Kumar","Suresh Reddy","Venkat Rao","Srinivas Naidu","Rajesh Babu","Kiran Kumar",
    "Arun Prasad","Mahesh Varma","Lokesh Reddy","Praveen Goud","Naveen Kumar","Ajay Reddy",
    "Deepak Rao","Harish Naidu","Ramesh Kumar","Srikanth Reddy","Vamshi Krishna","Sandeep Rao",
    "Priya Sharma","Anjali Reddy","Lakshmi Devi","Sunitha Rao","Padma Kumari","Sravani Reddy",
    "Meena Kumari","Kavitha Rao","Shalini Devi","Nandini Reddy","Bharathi Devi","Saritha Naidu",
    "Radha Krishna","Gopal Rao","Narayana Swamy","Venkateswara Rao","Suryanarayana Murthy",
    "Bhaskar Reddy","Mohan Das","Prasad Kumar","Ashok Reddy","Vijay Kumar","Raji Reddy",
    "Chandra Mohan","Durga Prasad","Ramana Murthy","Sai Kiran","Balakrishna","Kishore Kumar",
    "Murali Krishna","Vineeth Kumar","Rohit Reddy","Tarun Kumar","Akash Reddy","Nikhil Rao",
    "Abhishek Kumar","Aditya Rao","Pavan Kalyan","Siddharth Reddy","Chaitanya Kumar",
    "Pooja Reddy","Divya Kumari","Swathi Devi","Manasa Rao","Bhavani Devi","Keerthi Reddy",
    "Yamini Sri","Tejaswi Naidu","Alekhya Rao","Sirisha Reddy","Nithya Kumari",
    "Padmanabha Rao","Subramanyam","Krishnamurthy","Venugopal Rao","Chakravarthy",
    "Umamaheswara","Satyanarayana","Viswanadham","Lakshmana Rao","Raghavendra",
]

def gen_vehicle_no():
    district = random.choice(AP_DISTRICT_CODES)
    letters = random.choice(LETTER_PAIRS)
    number = str(random.randint(1000, 9999))
    return f"{district}{letters}{number}"

# Generate 500 unique vehicles
existing = set(RTODatabase.objects.values_list('vehicle_number', flat=True))
to_add = []
generated = set()

while len(to_add) < 500:
    vn = gen_vehicle_no()
    if vn not in existing and vn not in generated:
        generated.add(vn)
        model, fuel = random.choice(MODELS)
        owner = random.choice(NAMES)
        import datetime
        
        # Extract district code from vehicle number
        try:
            dist_code = int(vn[2:4])
        except:
            dist_code = 1
            
        # Series-based year mapping (2011-2024)
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
        reg_date = start_date + datetime.timedelta(days=random.randrange(days))
        
        to_add.append(RTODatabase(
            vehicle_number=vn,
            owner_name=owner,
            vehicle_model=model,
            fuel_type=fuel,
            registration_date=reg_date
        ))

RTODatabase.objects.bulk_create(to_add, ignore_conflicts=True)

total = RTODatabase.objects.count()
print(f"Added 500 vehicles. Total RTO DB count: {total}")
