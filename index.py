import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client, Client

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def home():
    try:
        res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
        bio_text = res.data[0]['bio'] if res.data else "Il manifesto è in fase di caricamento..."
    except:
        bio_text = "Connessione al database in corso..."
    
    return HTMLResponse(content=f"""
    <html>
    <head>
        <title>The American Way</title>
        <style>
            body {{ background-color: #000; color: #fff; text-align: center; font-family: 'Georgia', serif; padding-top: 100px; }}
            h1 {{ font-size: 4rem; text-transform: uppercase; border-bottom: 2px solid #fff; display: inline-block; padding-bottom: 10px; }}
            .content {{ max-width: 800px; margin: 50px auto; font-size: 1.5rem; line-height: 1.6; text-align: justify; }}
        </style>
    </head>
    <body>
        <h1>THE AMERICAN WAY</h1>
        <div class="content">{{bio_text}}</div>
    </body>
    </html>
    """)
