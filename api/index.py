import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

class BioUpdate(BaseModel):
    text: str

@app.get("/api/content")
async def get_content():
    # Prende Bio e Articoli dal database
    bio = supabase.table('profiles').select("bio").execute()
    articles = supabase.table('articles').select("*").order('created_at', desc=True).execute()
    return {"bio": bio.data[0]['bio'] if bio.data else "", "articles": articles.data}

@app.post("/api/admin/update-bio")
async def update_bio(data: BioUpdate):
    # Questo è quello che userai dal pannello Admin
    supabase.table('profiles').update({"bio": data.text}).eq("id", 1).execute()
    return {"status": "updated"}
