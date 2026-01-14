from flask import Flask, jsonify
from supabase import create_client
import os

app = Flask(__name__)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

@app.route('/')
def home():
    return "The American Way v3 - Online!"

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "database": "supabase"})

if __name__ == '__main__':
    app.run()
