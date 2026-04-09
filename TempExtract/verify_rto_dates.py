import sqlite3

def verify():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    
    serials = [
        ('AP05', 2011, 2014),
        ('AP18', 2014, 2018),
        ('AP39', 2018, 2021),
        ('AP45', 2021, 2024),
    ]
    
    print("Verification of Registration Dates by AP Series (District):")
    for series, start, end in serials:
        c.execute(f"SELECT vehicle_number, registration_date FROM seller_rtodatabase WHERE vehicle_number LIKE '{series}%' LIMIT 3")
        rows = c.fetchall()
        print(f"\n--- {series} Series (Target Year Range: {start} to {end}) ---")
        if rows:
            for vn, date in rows:
                print(f"Vehicle: {vn} -> Date: {date}")
        else:
            print("No records found for this series.")
    
    conn.close()

if __name__ == "__main__":
    verify()
