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
    res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
    bio_text = res.data[0]['bio'] if res.data else "Analisi in corso..."
    
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The American Way | Politica e Strategia</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&family=Oswald:wght@700&family=Georgia&display=swap" rel="stylesheet">
        <style>
            :root {{
                --brand-red: #e60000;
                --text-gray: #cccccc;
                --border-color: #333333;
            }}

            body {{
                background-color: #050505;
                color: #ffffff;
                margin: 0;
                font-family: 'Georgia', serif;
                line-height: 1.6;
            }}

            /* Sfondo con bandiere sbiadite in overlay */
            .bg-overlay {{
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: 
                    linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)),
                    url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
                z-index: -2;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(0,0,0,0.7);
                border-left: 1px solid var(--border-color);
                border-right: 1px solid var(--border-color);
                min-height: 100vh;
            }}

            /* Testata Stile New York Post */
            header {{
                padding: 30px 20px;
                text-align: center;
                border-bottom: 5px solid var(--brand-red);
            }}

            h1 {{
                font-family: 'Playfair Display', serif;
                font-size: clamp(3rem, 10vw, 6rem);
                color: var(--brand-red);
                text-transform: uppercase;
                margin: 0;
                letter-spacing: -3px;
                -webkit-text-stroke: 1.5px #fff;
                font-style: italic;
                line-height: 1;
            }}

            .tagline {{
                font-family: 'Oswald', sans-serif;
                text-transform: uppercase;
                letter-spacing: 5px;
                font-size: 1rem;
                margin-top: 10px;
                color: #fff;
            }}

            /* Spazio Pubblicità Top */
            .ad-leaderboard {{
                width: 100%;
                height: 90px;
                background: #111;
                margin: 20px 0;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px dashed #444;
                font-size: 0.8rem;
                color: #444;
            }}

            /* Layout a due colonne */
            .main-content {{
                display: grid;
                grid-template-columns: 1fr 300px;
                gap: 30px;
                padding: 20px 40px;
            }}

            .manifesto-section {{
                padding-right: 20px;
            }}

            .manifesto-title {{
                font-family: 'Oswald', sans-serif;
                font-size: 0.9rem;
                background: var(--brand-red);
                padding: 4px 12px;
                display: inline-block;
                margin-bottom: 25px;
            }}

            .text-body {{
                font-size: 1.35rem;
                text-align: justify;
                color: var(--text-gray);
                white-space: pre-wrap;
            }}

            /* Sidebar per Monetizzazione e News */
            .sidebar {{
                border-left: 1px solid var(--border-color);
                padding-left: 25px;
            }}

            .ad-sidebar {{
                width: 100%;
                height: 250px;
                background: #111;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px dashed #444;
                color: #444;
            }}

            .sidebar-title {{
                font-family: 'Oswald', sans-serif;
                border-bottom: 2px solid var(--brand-red);
                padding-bottom: 5px;
                margin-bottom: 15px;
                font-size: 1.1rem;
            }}

            @media (max-width: 900px) {{
                .main-content {{ grid-template-columns: 1fr; }}
                .sidebar {{ border-left: none; padding-left: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="bg-overlay"></div>
        <div class="container">
            <header>
                <h1>The American Way</h1>
                <div class="tagline">Intelligence • Strategy • Freedom</div>
            </header>

            <div class="ad-leaderboard">SPAZIO PUBBLICITARIO (LEADERBOARD 728x90)</div>

            <main class="main-content">
                <section class="manifesto-section">
                    <div class="manifesto-title">IL MANIFESTO</div>
                    <article class="text-body">{bio_text}</article>
                </section>

                <aside class="sidebar">
                    <div class="sidebar-title">MONETIZATION AREA</div>
                    <div class="ad-sidebar">ADV 300x250</div>
                    
                    <div class="sidebar-title">STRATEGIC INSIGHTS</div>
                    <p style="font-size: 0.9rem; color: #666;">Prossimamente: Analisi sul futuro della difesa europea.</p>
                </aside>
            </main>
        </div>
    </body>
    </html>
    """)
