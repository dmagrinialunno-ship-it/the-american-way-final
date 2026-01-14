import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()

# Connessione al tuo database Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

class BioUpdate(BaseModel):
    text: str

@app.get("/api/bio")
async def get_bio():
    # Legge il manifesto dal database
    response = supabase.table('profiles').select("bio").execute()
    return response.data[0] if response.data else {"bio": "Benvenuti su The American Way."}

@app.post("/api/admin/update-bio")
async def update_bio(data: BioUpdate):
    # Permette di aggiornare il manifesto dall'area admin
    supabase.table('profiles').update({"bio": data.text}).eq("id", 1).execute()
    return {"status": "success"}
