# 404Ghost 👻

Ever wonder how phishing attacks actually work under the hood?

I built 404Ghost to find out. Instead of downloading a ready-made tool like Evilginx, I built everything from scratch — reverse proxy, fake login pages, credential capture, session hijacking — all of it. One command and the whole lab is running.

---

## What 404Ghost Does

404Ghost is a phishing simulation lab. You spin it up, send someone a link, they land on a fake login page, enter their credentials and you get an instant Telegram notification on your phone. Meanwhile mitmproxy is sitting in the middle stealing session cookies — which means even if they have MFA enabled, you still get in.

This is exactly how real attackers operate. 404Ghost lets you study and simulate that in a safe controlled environment.

---

## Built With

- **Docker** — everything runs in containers, one command to start
- **Traefik** — handles all incoming traffic and SSL. If you have a domain from [FreeDNS](https://freedns.afraid.org) and deploy on a VPS, Traefik will automatically get a real SSL certificate via Let's Encrypt. Running locally? Traefik still routes traffic cleanly on port 80 so your URL looks like `/login` instead of `:5000/login`
- **Flask** — serves the fake pages and captures credentials
- **mitmproxy** — intercepts traffic and steals session cookies. Requires your browser to be configured to use it as a proxy on port 8082
- **Telegram** — sends you real time alerts when credentials are captured

---

## Requirements

Before you start make sure you have the following installed:

- **Docker** — [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** — included with Docker Desktop. On Linux run:
```
curl -fsSL https://get.docker.com | sudo sh
```
docker --version
docker compose version
```

---

## Installation

# Clone the repository
git clone https://github.com/404Ghost-security/404Ghost.git

# Navigate into the project
cd 404Ghost

# Copy the environment template
cp .env.example .env

# Edit the .env file with your values
nano .env

# Start the lab
docker compose up -d

# Verify all containers are running
docker ps
```

Then open your browser:

| What | Where |
|------|-------|
| Fake login page | http://YOUR_IP/login |
| Traefik dashboard | http://YOUR_IP:8080 |
| mitmproxy UI | http://YOUR_IP:8081 |

---

## Setting Up Telegram Notifications

404Ghost sends you real time alerts on your phone via Telegram when someone submits credentials. Here is how to set it up:

### Step 1 — Create a Telegram Bot

1. Open Telegram on your phone or browser
2. Search for **@BotFather**
3. Send the message `/newbot`
4. Give your bot a name — example: `404Ghost Bot`
5. Give your bot a username — must end in `bot`, example: `ghost404_bot`
6. BotFather will send you a token that looks like this:

123456789:ABCdefGHIjklMNOpqrSTUvwxYZ

7. Copy and save this token — this is your `TELEGRAM_BOT_TOKEN`

### Step 2 — Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Send it any message
3. It will reply with your ID that looks like:

123456789

4. Copy and save this number — this is your `TELEGRAM_CHAT_ID`

### Step 3 — Start A Conversation With Your Bot

1. Search for your bot by the username you created
2. Click **Start**
3. Send it any message
4. This step is required — your bot cannot send you messages until you start a conversation first

### Step 4 — Add To .env File

Open your `.env` file and fill in:

TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE


---

## View Captured Credentials

After a victim logs in you can check what was captured:

```
cat ~/404Ghost/flask/logs/credentials.log
```

---

## Local vs VPS Deployment

| Feature | Local Kali | VPS + FreeDNS |
|---------|-----------|---------------|
| SSL padlock | ❌ | ✅ |
| Real domain | ❌ | ✅ |
| Google OAuth capture | ❌ | ✅ |
| Credential capture | ✅ | ✅ |
| Telegram alerts | ✅ | ✅ |
| MFA bypass | ✅ | ✅ |
| mitmproxy | ✅ browser config needed | ✅ |

> **Note:** Running locally the Google SSO button will show an unavailability message. For full Google OAuth capture and a real SSL padlock deploy on a VPS with a domain from [FreeDNS](https://freedns.afraid.org) and Traefik will handle the SSL certificate automatically.

---

## mitmproxy Setup

To capture session cookies and traffic with mitmproxy:

1. Configure your browser proxy settings:
   - HTTP Proxy: `YOUR_IP`
   - Port: `8082`
2. With the proxy configured open your browser and go to:
   `http://mitm.it`
   This only works AFTER configuring the proxy
3. Download and install the certificate for your OS:
   - **Windows** → click Windows and install the certificate
   - **macOS** → click macOS and install the certificate
   - **Linux** → click Linux and follow the instructions
   - **iOS** → click iOS and install the profile
   - **Android** → click Android and install the certificate
4. Visit the target site — all traffic will now be captured
5. View captures at `http://YOUR_IP:8081` with password `admin123`

---

## What This Is Good For

- Security awareness training
- Teaching employees to spot phishing
- Red team practice in authorized environments
---

## Important

Only use this on systems you own or have written permission to test. Unauthorized use is illegal. This project exists for education and authorized testing only.

---

## Demo

🎥 [Watch the full demo on YouTube](#) — add your link here after uploading

---

## About

I also wrote **Yon Sèl Klik** — a digital security guide written in Haitian Creole for people who want to protect themselves online.

🌐 [yonselklik.com](https://yonselklik.com)
