import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/api/bio")
async def get_bio():
    res = supabase.table('profiles').select("bio").execute()
    return res.data[0] if res.data else {"bio": "Errore: Bio non trovata"}
