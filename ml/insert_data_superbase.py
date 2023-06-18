import csv
import os
from supabase import create_client, Client

url: str = "https://pjaybbjalewghaqmkhzq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqYXliYmphbGV3Z2hhcW1raHpxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NjcyMDgyMiwiZXhwIjoyMDAyMjk2ODIyfQ.6KVQbT9mE4RVvUo2j_zLxM7RFTwF8HR3NAgj2fU-ERs"
supabase: Client = create_client(url, key)

# data = supabase.table("nltk").insert({"PROVINCE_CODE":"ON"}).execute()
# assert len(data.data) > 0

key = ["ID","DATE","PROVINCE_CODE","LATITUDE","LONGITUDE","CAUSE","SIZE_HA","OUT_DATE","YEAR","MONTH","DAY","text"]

with open('./nltk.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            
            for row in reader:
              if row[2] == 'Ontario' and int(row[0]) > 268572:
                obj = {
                  "ID": row[0],
                  "DATE": row[1],
                  "PROVINCE_CODE": row[2],
                  "LATITUDE": row[3],
                  "LONGITUDE": row[4],
                  "CAUSE": row[5],
                  "SIZE_HA": row[6],
                  "OUT_DATE": row[7],
                  "YEAR": row[8],
                  "MONTH": row[9],
                  "DAY": row[10],
                  "text": row[11]
                }
                data = supabase.table("nltk").insert(obj).execute()
              
print('done')
