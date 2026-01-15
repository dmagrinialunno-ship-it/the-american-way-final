import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase import create_client, Client

app = FastAPI()

# Connessione Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# --- STILI CSS COMUNI (Stile NY Post / NY Times) ---
COMMON_STYLE = """
<style>
    :root { --brand-red: #e60000; --bg-black: #0a0a0a; --text-light: #f4f4f4; }
    body { background: var(--bg-black); color: var(--text-light); font-family: 'Georgia', serif; margin: 0; }
    .container { max-width: 1200px; margin: 0 auto; border-left: 1px solid #222; border-right: 1px solid #222; min-height: 100vh; }
    header { padding: 40px 20px; text-align: center; border-bottom: 5px solid var(--brand-red); background: rgba(0,0,0,0.9); }
    h1 { font-family: 'Playfair Display', serif; font-size: 5.5rem; color: var(--brand-red); text-transform: uppercase; margin: 0; -webkit-text-stroke: 1.5px white; letter-spacing: -3px; font-style: italic; }
    .nav-bar { background: #111; padding: 10px; text-align: center; border-bottom: 1px solid #333; font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; }
    .nav-bar a { color: #888; text-decoration: none; margin: 0 15px; }
    .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; padding: 30px; }
    .section-title { font-family: 'Oswald', sans-serif; background: var(--brand-red); color: white; padding: 5px 15px; display: inline-block; margin-bottom: 20px; }
    .ad-placeholder { background: #111; border: 1px dashed #444; color: #444; text-align: center; padding: 20px; margin: 20px 0; font-size: 0.7rem; }
    input, textarea { width: 100%; padding: 15px; background: #111; border: 1px solid #333; color: white; margin-bottom: 20px; font-family: 'Georgia', serif; }
    .btn { background: var(--brand-red); color: white; padding: 10px 30px; border: none; cursor: pointer; text-transform: uppercase; font-weight: bold; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&family=Oswald:wght@400;700&display=swap" rel="stylesheet">
"""

# --- ROTTA 1: HOME PAGE ---
@app.get("/")
async def home():
    res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
    bio = res.data[0]['bio'] if res.data else "In attesa del manifesto..."
    
    return HTMLResponse(content=f"""
    <html>
    <head><title>The American Way</title>{COMMON_STYLE}</head>
    <body>
        <div class="container">
            <div class="nav-bar">
                <a href="/">Home</a> | <a href="/admin">Admin Access</a> | 2026 Strategy
            </div>
            <header><h1>The American Way</h1></header>
            <div class="ad-placeholder">ADV LEADERBOARD 728x90</div>
            <main class="grid">
                <section>
                    <div class="section-title">Il Manifesto</div>
                    <div style="font-size: 1.4rem; line-height: 1.8; text-align: justify;">{bio}</div>
                </section>
                <aside>
                    <div class="section-title">Latest Intelligence</div>
                    <div class="ad-placeholder" style="height: 300px;">ADV BOX 300x250</div>
                    <p style="color: #666; font-style: italic;">Analisi sulla burocrazia europea in arrivo...</p>
                </aside>
            </main>
        </div>
    </body>
    </html>
    """)

# --- ROTTA 2: AREA ADMIN (La tua plancia di comando) ---
@app.get("/admin")
async def admin_page():
    return HTMLResponse(content=f"""
    <html>
    <head><title>Admin | The American Way</title>{COMMON_STYLE}</head>
    <body>
        <div class="container" style="max-width: 800px; padding: 40px;">
            <div class="section-title">Dashboard Editoriale</div>
            <h2>Aggiorna il Manifesto</h2>
            <form action="/publish" method="post">
                <textarea name="content" rows="15" placeholder="Scrivi qui il tuo nuovo manifesto o articolo..."></textarea>
                <button type="submit" class="btn">Pubblica Istantaneamente</button>
            </form>
            <p><a href="/" style="color: #666;">Torna al sito</a></p>
        </div>
    </body>
    </html>
    """)

# --- ROTTA 3: LOGICA DI PUBBLICAZIONE ---
@app.post("/publish")
async def publish(content: str = Form(...)):
    # Inserisce il nuovo testo nel database
    supabase.table('profiles').insert({"bio": content}).execute()
    return RedirectResponse(url="/", status_code=303)
