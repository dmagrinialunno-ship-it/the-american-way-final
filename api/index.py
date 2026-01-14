import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/api/bio")
async def get_bio():
    # Prende la bio dalla riga con ID 1 che abbiamo lasciato su Supabase
    res = supabase.table('profiles').select("bio").eq("id", 1).execute()
    if res.data:
        return {"bio": res.data[0]['bio']}
    return {"bio": "Manifesto in fase di caricamento..."}
