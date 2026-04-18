import os
import requests
from fastapi import FastAPI
from supabase import create_client

app = FastAPI()

# ดึงค่าจาก Vercel Environment Variables
URL = os.environ.get("URL")
KEY = os.environ.get("KEY")
LOYVERSE_TOKEN = os.environ.get("LOYVERSE_TOKEN")

supabase = create_client(URL, KEY)

@app.get("/sync")
async def sync_data():
    headers = {"Authorization": f"Bearer {LOYVERSE_TOKEN}"}
    try:
        # 1. ดึงข้อมูลจาก Loyverse
        response = requests.get("https://api.loyverse.com/v1.0/receipts", headers=headers)
        if response.status_code != 200:
            return {"status": "error", "message": "Loyverse API error"}

        receipts = response.json().get("receipts", [])
        
        # 2. ส่งข้อมูลไป Supabase (ใช้ตารางชื่อ loyverse_sales)
        for rc in receipts:
            # ใช้คอลัมน์เดียวชื่อ 'payload' เพื่อเก็บข้อมูลทั้งหมดเป็น JSON
            supabase.table("loyverse_sales").insert({"payload": rc}).execute()
            
        return {"status": "success", "count": len(receipts)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}