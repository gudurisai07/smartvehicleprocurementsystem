import requests

def test_rest():
    url = "https://onacqqlmieerzhghfhcm.supabase.co/rest/v1"
    headers = {
        "apikey": "sb_publishable_4HIEbxBjC33JQzqJIXuCtA_QHqRkvsP",
        "Authorization": "Bearer sb_publishable_4HIEbxBjC33JQzqJIXuCtA_QHqRkvsP",
        "Range": "0-9"
    }
    
    tables_to_try = [
        "vehicle_table", "Vehicle_Table", "Vehicle Table", "vehicletable",
        "vehicle_details", "VehicleDetails",
        "rto_database", "RTODatabase", "rto", "RTO", 
        "vahan", "Vahan", "vahan_database",
        "vehicles", "Vehicles", "vehicle", "Vehicle",
        "rto_table", "RTOTable", "cars", "Cars"
    ]
    
    for table in tables_to_try:
        try:
            safe_table = requests.utils.quote(table)
            res = requests.get(f"{url}/{safe_table}?select=*", headers=headers)
            
            if res.status_code == 200:
                print(f"FOUND TABLE: {table}")
                print(res.json())
                return
        except:
            pass
            
    print("NOTHING FOUND")

if __name__ == "__main__":
    test_rest()
