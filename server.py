from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)
app.secret_key = "learn_with_iss_clean_platform_secure_key"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

POST_FILE = "posts.txt"
SHOP_FILE = "shop_items.txt"
INQUIRY_FILE = "inquiries.txt"
ADMIN_LIST_FILE = "admins.txt"

def load_posts():
    posts = []
    if os.path.exists(POST_FILE):
        with open(POST_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|||")
                if len(parts) >= 5:
                    posts.append({"id": parts[0], "author": parts[1], "content": parts[2], "img": parts[3], "date": parts[4]})
    return posts

def load_shop():
    return [
        {"id": "SH-01", "name": "Advanced Wireless Pentest Adapter", "price": "৳ 2,800", "img": "https://i.imgur.com/6VBx3io.png"},
        {"id": "SH-02", "name": "Cyber Defense Operator Hoodie", "price": "৳ 1,950", "img": "https://i.imgur.com/6VBx3io.png"},
        {"id": "SH-03", "name": "Hardware Emulation & Payload Tool", "price": "৳ 3,500", "img": "https://i.imgur.com/6VBx3io.png"}
    ]

@app.route("/", methods=["GET", "POST"])
def home():
    posts = load_posts()
    shop_items = load_shop()
    msg = ""

    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "contact":
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")
            if name and email:
                with open(INQUIRY_FILE, "a") as f:
                    f.write(f"{name}|{email}|{message}|{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                msg = "✅ Your transmission has been received securely."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Learn with ISS | Cybersecurity Training & Infrastructure Defense</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --bg-primary: #050814; --bg-secondary: #0a0f1d; --bg-card: #0f172a;
                --accent-blue: #0284c7; --accent-hover: #0369a1; --text-main: #f1f5f9;
                --text-muted: #64748b; --border-color: #1e293b;
            }
            body { font-family: 'Inter', system-ui, sans-serif; background-color: var(--bg-primary); color: var(--text-main); margin: 0; padding: 0; scroll-behavior: smooth; }
            .navbar { display: flex; justify-content: space-between; align-items: center; padding: 20px 8%; border-bottom: 1px solid var(--border-color); background: rgba(5, 8, 20, 0.95); position: sticky; top: 0; z-index: 1000; backdrop-filter: blur(8px); }
            .logo { font-size: 19px; font-weight: 700; color: var(--text-main); text-decoration: none; letter-spacing: 0.5px; text-transform: uppercase; }
            .logo span { color: var(--accent-blue); }
            .nav-links { display: flex; gap: 28px; align-items: center; }
            .nav-links a { color: var(--text-muted); text-decoration: none; font-size: 13px; font-weight: 500; transition: color 0.2s; }
            .nav-links a:hover { color: var(--accent-blue); }
            .hero { text-align: center; padding: 110px 20px; background: radial-gradient(circle at center, #0a1128 0%, #050814 70%); border-bottom: 1px solid var(--border-color); }
            .hero h1 { font-size: 44px; margin-bottom: 12px; font-weight: 800; letter-spacing: -0.5px; }
            .hero p { color: var(--accent-blue); font-size: 17px; font-weight: 500; margin-bottom: 30px; letter-spacing: 0.2px; }
            .container { max-width: 1000px; margin: 50px auto; padding: 0 20px; }
            .section-title { font-size: 22px; font-weight: 700; margin-bottom: 25px; border-left: 3px solid var(--accent-blue); padding-left: 12px; letter-spacing: -0.3px; }
            .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 22px; margin-bottom: 40px; }
            .card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 28px; box-shadow: 0 4px 25px rgba(0,0,0,0.4); }
            input, textarea { width: 100%; padding: 13px; margin: 8px 0 16px 0; background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 6px; color: white; box-sizing: border-box; font-size: 14px; }
            button { background: var(--accent-blue); color: white; border: none; padding: 13px 26px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 14px; }
            button:hover { background: var(--accent-hover); }
            footer { border-top: 1px solid var(--border-color); background: var(--bg-secondary); padding: 45px 20px; text-align: center; color: var(--text-muted); font-size: 13px; }
            .social-icons { display: flex; justify-content: center; gap: 22px; margin-bottom: 18px; font-size: 20px; }
            .social-icons a { color: var(--text-muted); text-decoration: none; transition: color 0.2s; }
            .social-icons a:hover { color: var(--accent-blue); }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <a href="/" class="logo">LEARN WITH <span>ISS</span></a>
            <div class="nav-links">
                <a href="#about">Overview</a>
                <a href="#shop">Hardware & Tools</a>
                <a href="#blog">Security Feed</a>
                <a href="#contact">Direct Contact</a>
                <a href="/client-login" style="background:var(--accent-blue); color:white; padding:8px 18px; border-radius:6px;">Client Portal</a>
            </div>
        </nav>

        <div class="hero">
            <h1>Learn with ISS</h1>
            <p>Offensive Security Methodologies | Infrastructure Defense & Vulnerability Research</p>
            <a href="#shop" style="background:var(--accent-blue); color:white; padding:13px 30px; border-radius:6px; text-decoration:none; font-weight:600; display:inline-block; font-size:14px;">Explore Solutions</a>
        </div>

        <div class="container">
            <div class="card" id="about" style="margin-bottom: 45px;">
                <h3 class="section-title">Platform Overview</h3>
                <p style="color: var(--text-muted); line-height: 1.7; font-size: 15px;">
                    Learn with ISS specializes in enterprise security auditing, advanced penetration testing frameworks, and defensive architecture hardening. Focused on identifying systemic vulnerabilities before exploitation and constructing robust operational safeguards across cloud environments.
                </p>
            </div>

            <div id="shop">
                <h3 class="section-title">⚡ Security Hardware & Testing Gears</h3>
                <div class="grid-3">
                    {% for item in shop_items %}
                    <div class="card" style="text-align: center;">
                        <img src="{{ item.img }}" style="width:100%; height:160px; object-fit:cover; border-radius:6px; margin-bottom:15px; border: 1px solid var(--border-color);">
                        <h4 style="margin: 0 0 8px 0; font-size: 16px;">{{ item.name }}</h4>
                        <p style="color:var(--accent-blue); font-weight:600; font-size:15px; margin:0 0 18px 0;">{{ item.price }}</p>
                        <a href="#contact" style="display:inline-block; background:var(--bg-secondary); color:#38bdf8; padding:9px 18px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:600; border: 1px solid var(--border-color);">Inquire Availability</a>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="blog" style="margin-top: 50px;">
                <h3 class="section-title">📡 Threat Intelligence & Security Logs</h3>
                {% if posts %}
                    {% for p in posts %}
                    <div class="card" style="margin-bottom: 18px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:13px;">
                            <b style="color: var(--accent-blue);">{{ p.author }}</b> <span style="color:var(--text-muted);">{{ p.date }}</span>
                        </div>
                        <p style="margin:0; font-size:14px; line-height: 1.6;">{{ p.content }}</p>
                        {% if p.img %}<img src="{{ p.img }}" style="max-width:100%; border-radius:6px; margin-top:12px;" />{% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="color:var(--text-muted); font-size:14px;">No active broadcast logs found.</p>
                {% endif %}
            </div>

            <div id="contact" style="margin-top: 60px;">
                <h3 class="section-title">Secure Communication Channel</h3>
                {% if msg %}<div style="background: rgba(2, 132, 199, 0.1); border: 1px solid var(--accent-blue); color: #38bdf8; padding: 13px; border-radius: 6px; margin-bottom: 20px; font-size: 13px;">{{ msg }}</div>{% endif %}
                <div class="card">
                    <form method="POST">
                        <input type="hidden" name="form_type" value="contact">
                        <label style="font-size:12px; color:var(--text-muted); font-weight:500;">Name / Entity</label>
                        <input type="text" name="name" required>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:500;">Secure Email</label>
                        <input type="email" name="email" required>
                        <label style="font-size:12px; color:var(--text-muted); font-weight:500;">Payload / Message</label>
                        <textarea name="message" rows="4" required></textarea>
                        <button type="submit">Transmit Inquiry</button>
                    </form>
                </div>
            </div>
        </div>

        <footer>
            <div class="social-icons">
                <a href="https://github.com" target="_blank"><i class="fa-brands fa-github"></i></a>
                <a href="https://linkedin.com" target="_blank"><i class="fa-brands fa-linkedin"></i></a>
                <a href="https://twitter.com" target="_blank"><i class="fa-brands fa-twitter"></i></a>
            </div>
            <p>&copy; 2026 Learn with ISS. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """, shop_items=shop_items, posts=posts, msg=msg)

@app.route("/client-login")
def client_login():
    return "<body style='background:#050814; color:#f1f5f9; font-family:Inter; text-align:center; padding-top:100px;'><h3>Client Authentication Gateway</h3><p><a href='/' style='color:#0284c7; text-decoration:none;'>&larr; Return to Main Interface</a></p></body>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
