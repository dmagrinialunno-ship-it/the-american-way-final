import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client, Client

app = FastAPI()

# Configurazione Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

@app.get("/")
async def home():
    # Recupero Bio/Manifesto
    try:
        res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
        bio_text = res.data[0]['bio'] if res.data else "Il manifesto è in fase di caricamento..."
    except:
        bio_text = "Connessione al database in corso..."

    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The American Way | Strategia e Potere</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&family=Oswald:wght@700&family=Georgia&family=Roboto+Condensed:wght@700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --blood-red: #cc0000;
                --paper-white: #f4f4f4;
                --dark-bg: #0a0a0a;
            }}

            body {{
                background-color: var(--dark-bg);
                color: var(--paper-white);
                margin: 0;
                font-family: 'Georgia', serif;
                overflow-x: hidden;
            }}

            /* Sfondo con bandiere sbiadite (Overlay) */
            .background-flags {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: 
                    linear-gradient(rgba(10,10,10,0.9), rgba(10,10,10,0.9)),
                    url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
                z-index: -1;
                display: flex;
                justify-content: space-between;
                opacity: 0.3; /* Effetto sbiadito */
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(0,0,0,0.8);
                border-left: 1px solid #222;
                border-right: 1px solid #222;
                min-height: 100vh;
                box-shadow: 0 0 50px rgba(0,0,0,1);
            }}

            /* Header Stile New York Post */
            header {{
                padding: 40px 20px;
                text-align: center;
                border-bottom: 6px double #333;
            }}

            .masthead h1 {{
                font-family: 'Playfair Display', serif;
                font-size: clamp(3.5rem, 12vw, 7rem);
                color: var(--blood-red);
                text-transform: uppercase;
                margin: 0;
                letter-spacing: -4px;
                -webkit-text-stroke: 1.8px #fff; /* Contorno bianco */
                font-style: italic;
                line-height: 0.9;
                filter: drop-shadow(5px 5px 0px rgba(0,0,0,1));
            }}

            .tagline-bar {{
                border-top: 1px solid #444;
                border-bottom: 1px solid #444;
                margin-top: 20px;
                padding: 8px 0;
                font-family: 'Oswald', sans-serif;
                text-transform: uppercase;
                letter-spacing: 6px;
                font-size: 0.85rem;
                color: #888;
            }}

            /* Area Monetizzazione (Header) */
            .ad-top {{
                width: 100%;
                max-width: 728px;
                height: 90px;
                margin: 20px auto;
                background: #111;
                border: 1px dashed #333;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Oswald', sans-serif;
                font-size: 0.7rem;
                color: #444;
            }}

            /* Layout Griglia */
            main {{
                display: grid;
                grid-template-columns: 1fr 320px;
                gap: 40px;
                padding: 40px;
            }}

            .main-column {{
                border-right: 1px solid #222;
                padding-right: 20px;
            }}

            .section-label {{
                font-family: 'Roboto Condensed', sans-serif;
                background: var(--blood-red);
                color: #fff;
                padding: 4px 12px;
                display: inline-block;
                text-transform: uppercase;
                margin-bottom: 30px;
                font-size: 0.9rem;
            }}

            .article-content {{
                font-size: 1.4rem;
                line-height: 1.8;
                color: #ddd;
                text-align: justify;
                white-space: pre-wrap;
            }}

            /* Sidebar Monetizzazione */
            .sidebar-ad {{
                width: 300px;
                height: 600px; /* Skyscraper ad format */
                background: #111;
                border: 1px dashed #333;
                margin-top: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Oswald', sans-serif;
                font-size: 0.7rem;
                color: #444;
                position: sticky;
                top: 20px;
            }}

            @media (max-width: 900px) {{
                main {{ grid-template-columns: 1fr; }}
                .main-column {{ border-right: none; padding-right: 0; }}
                .sidebar {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="background-flags"></div>
        <div class="container">
            <header>
                <div class="masthead">
                    <h1>The American Way</h1>
                </div>
                <div class="tagline-bar">
                    Intelligence • Strategy • Freedom — 2026
                </div>
            </header>

            <div class="ad-top">SPAZIO PUBBLICITARIO DISPONIBILE (728x90)</div>

            <main>
                <div class="main-column">
                    <div class="section-label">Il Manifesto Strategico</div>
                    <article class="article-content">{bio_text}</article>
                </div>

                <aside class="sidebar">
                    <div class="section-label" style="background: #333;">Monetizzazione</div>
                    <div class="sidebar-ad">SPAZIO PUBBLICITARIO (300x600)</div>
                </aside>
            </main>
        </div>
    </body>
    </html>
    """)
