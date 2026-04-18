from fastapi import FastAPI, Request
from supabase import create_client

app = FastAPI()

# นำ URL และ Key จากหน้า API Settings ใน Supabase มาใส่ที่นี่
URL = "https://xlfeqhpeddgjryywkheo.supabase.co"
KEY = "sb_secret_qlDd3N89redY1nZYawGIZQ_vraEQT5c"
supabase = create_client(URL, KEY)

@app.post("/webhook")
async def loyverse_webhook(request: Request):
    # 1. รับข้อมูลที่ Loyverse ส่งมา
    payload = await request.json()
    
    # 2. บันทึกข้อมูลลงตาราง loyverse_sales (ที่เราสร้างในข้อ 1)
    # เราเก็บทั้งก้อนลงในคอลัมน์ชื่อ 'payload' (ประเภท jsonb)
    data = {
        "payload": payload,
        "receipt_id": payload.get("receipt_number") # ตัวอย่างการดึงค่าบางอย่างออกมาเก็บ
    }
    
    response = supabase.table("loyverse_sales").insert(data).execute()
    
    return {"status": "success"}