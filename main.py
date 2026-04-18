import os
import requests
from fastapi import FastAPI
from supabase import create_client

app = FastAPI()

# ดึงค่าจาก Settings ที่เราเพิ่งกรอกไป
URL = os.environ.get("URL")
KEY = os.environ.get("KEY")
LOYVERSE_TOKEN = os.environ.get("LOYVERSE_TOKEN")

supabase = create_client(URL, KEY)

@app.get("/")
async def root():
    return {"message": "System is running!"}

# สร้างทางลัดไว้กดเพื่อดึงข้อมูล (Sync)
@app.get("/sync")
async def sync_data():
    headers = {"Authorization": f"Bearer {LOYVERSE_TOKEN}"}
    # ดึงข้อมูลใบเสร็จล่าสุดจาก Loyverse
    response = requests.get("https://api.loyverse.com/v1.0/receipts", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        receipts = data.get("receipts", [])
        
        # ส่งข้อมูลเข้า Supabase
        for receipt in receipts:
            supabase.table("loyverse_sales").insert(receipt).execute()
            
        return {"status": "success", "synced_count": len(receipts)}
    else:
        return {"status": "error", "message": response.text}