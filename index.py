import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase import create_client, Client

app = FastAPI()

# Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# CSS Professionale - Stile "The Post"
CSS = """
<style>
    :root { --red: #cc0000; --gold: #c5a059; --bg: #050505; }
    body { background: var(--bg); color: #fff; font-family: 'Georgia', serif; margin: 0; padding: 0; }
    .top-nav { background: #111; padding: 10px; text-align: center; font-family: 'Arial', sans-serif; font-size: 0.7rem; letter-spacing: 2px; border-bottom: 1px solid #222; }
    .top-nav a { color: #888; text-decoration: none; margin: 0 15px; text-transform: uppercase; }
    
    header { text-align: center; padding: 50px 20px; border-bottom: 4px double #333; max-width: 1200px; margin: 0 auto; }
    h1 { font-family: 'Playfair Display', serif; font-size: 6rem; color: var(--red); text-transform: uppercase; margin: 0; -webkit-text-stroke: 1px #fff; font-style: italic; line-height: 0.8; }
    .tagline { font-family: 'Oswald', sans-serif; font-size: 1rem; letter-spacing: 8px; margin-top: 15px; color: #fff; }

    .main-grid { display: grid; grid-template-columns: 1fr 300px; gap: 40px; max-width: 1200px; margin: 40px auto; padding: 0 20px; }
    
    .content-area { border-right: 1px solid #222; padding-right: 40px; }
    .label { background: var(--red); color: #fff; padding: 4px 10px; font-family: sans-serif; font-size: 0.8rem; font-weight: bold; margin-bottom: 20px; display: inline-block; }
    .manifesto-text { font-size: 1.5rem; line-height: 1.7; text-align: justify; color: #ddd; }
    
    .sidebar { position: sticky; top: 20px; }
    .ad-box { background: #111; border: 1px dashed #444; height: 600px; display: flex; align-items: center; justify-content: center; color: #444; font-family: sans-serif; font-size: 0.8rem; }
    
    .admin-bar { position: fixed; bottom: 0; width: 100%; background: var(--red); padding: 10px; text-align: center; }
    .admin-bar a { color: #fff; font-weight: bold; text-decoration: none; font-family: sans-serif; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,900;1,900&family=Oswald:wght@700&display=swap" rel="stylesheet">
"""

@app.get("/")
async def home():
    res = supabase.table('profiles').select("bio").order('created_at', desc=True).limit(1).execute()
    bio = res.data[0]['bio'] if res.data else "Il Manifesto è in fase di caricamento dal database..."
    
    return HTMLResponse(content=f"""
    <html>
    <head><title>The American Way</title>{CSS}</head>
    <body>
        <div class="top-nav">
            <a href="#">Politics</a> <a href="#">Strategy</a> <a href="#">Defense</a> <a href="#">About</a>
        </div>
        <header>
            <h1>The American Way</h1>
            <div class="tagline">INTELLIGENCE • POWER • STRATEGY</div>
        </header>
        <main class="main-grid">
            <div class="content-area">
                <div class="label">EDITORIALE</div>
                <div class="manifesto-text">{bio}</div>
            </div>
            <aside class="sidebar">
                <div class="label" style="background:#333">ADVERTISING</div>
                <div class="ad-box">SPAZIO PUBBLICITARIO (MONETIZZAZIONE)</div>
            </aside>
        </main>
        <div class="admin-bar">
            <a href="/admin">ACCEDI ALL'AREA EDITORIALE SEGRETA</a>
        </div>
    </body>
    </html>
    """)

@app.get("/admin")
async def admin():
    return HTMLResponse(content=f"<html><head>{CSS}</head><body style='padding:50px'><div class='label'>ADMIN PANEL</div><form action='/publish' method='post'><textarea name='c' style='width:100%;height:300px;background:#111;color:#fff;padding:20px;font-size:1.2rem'></textarea><br><br><button type='submit' style='background:red;color:white;padding:15px 40px;border:none;cursor:pointer'>PUBBLICA ORA</button></form></body></html>")

@app.post("/publish")
async def publish(c: str = Form(...)):
    supabase.table('profiles').insert({"bio": c}).execute()
    return RedirectResponse(url="/", status_code=303)
