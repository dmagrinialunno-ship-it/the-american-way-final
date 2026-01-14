import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/api/bio")
async def get_bio():
    # Prova a prendere la prima riga disponibile in assoluto
    res = supabase.table('profiles').select("bio").limit(1).execute()
    if res.data and len(res.data) > 0:
        return {"bio": res.data[0]['bio']}
    return {"bio": "Il manifesto è in fase di pubblicazione. Controlla il database Supabase."}
