import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client, Client

app = FastAPI()

# Inizializzazione pulita
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def home():
    try:
        # Recupero l'ultimo testo inserito
        res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
        bio_text = res.data[0]['bio'] if res.data else "In attesa del manifesto..."
    except Exception as e:
        bio_text = "Connessione al database in corso..."

    return HTMLResponse(content=f"""
    <html>
    <head>
        <title>The American Way</title>
        <style>
            body {{ background: #000; color: #fff; font-family: 'Georgia', serif; text-align: center; padding-top: 100px; }}
            h1 {{ font-size: 3rem; text-transform: uppercase; border-bottom: 2px solid #fff; display: inline-block; padding-bottom: 10px; }}
            p {{ max-width: 800px; margin: 40px auto; font-size: 1.4rem; line-height: 1.6; text-align: justify; }}
        </style>
    </head>
    <body>
        <h1>THE AMERICAN WAY</h1>
        <p>{{bio_text}}</p>
    </body>
    </html>
    """)
