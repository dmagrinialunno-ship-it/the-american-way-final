import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client, Client

app = FastAPI()

# Collegamento al database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def home():
    # Prende l'ultima bio salvata su Supabase
    res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
    bio_text = res.data[0]['bio'] if res.data else "Manifesto in fase di caricamento..."
    
    # Genera la pagina stile New York Times direttamente da qui
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8"><title>The American Way</title>
        <style>
            body {{ background: #000; color: #fff; font-family: 'Georgia', serif; padding: 60px; line-height: 1.8; display: flex; justify-content: center; }}
            .container {{ max-width: 750px; }}
            h1 {{ font-size: 3.5rem; border-bottom: 3px solid #fff; padding-bottom: 10px; text-transform: uppercase; letter-spacing: -1px; }}
            .bio {{ font-size: 1.35rem; margin-top: 40px; white-space: pre-wrap; color: #ddd; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>The American Way</h1>
            <div class="bio">{bio_text}</div>
        </div>
    </body>
    </html>
    """)
