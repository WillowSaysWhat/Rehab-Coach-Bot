# Sugar Rehab Companion — Setup & Run Guide

This guide walks you from cloning the repository to running the app.

---

## 1. Prerequisites

- **Git** — to clone the repository
- **Python 3.10+** — the app is written in Python
- **uv** (recommended) — fast Python package manager and venv tool, or use built-in `venv` + `pip`

---

## 2. Clone the Repository

From a terminal (PowerShell, Command Prompt, or bash):

```bash
git clone https://github.com/YOUR_USERNAME/Rehab-Coach-Bot.git
cd Rehab-Coach-Bot
```

Replace `YOUR_USERNAME` with the actual GitHub username or organization.

---

## 3. Install uv (Recommended)

uv is used to create the virtual environment and install dependencies quickly.

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installing, restart your terminal or add uv to your PATH if needed (e.g. `~/.local/bin` on Linux/macOS, `%USERPROFILE%\.local\bin` on Windows).

---

## 4. Set Up the Virtual Environment

All commands in this section are run from the **Sugar_Rehab_Companion** folder.

### 4.1. Go to the app folder

```bash
cd Sugar_Rehab_Companion
```

### 4.2. Create the virtual environment (with uv)

```bash
uv venv
```

This creates a `.venv` directory using your system Python (e.g. 3.12).

**Alternative (without uv):** use Python’s built-in venv:

```bash
python -m venv .venv
```

### 4.3. Activate the virtual environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\activate
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

When active, your prompt usually starts with `(.venv)`.

### 4.4. Install dependencies

**With uv (from Sugar_Rehab_Companion, venv can be inactive):**

```bash
uv pip install -r requirements.txt --python .venv\Scripts\python.exe
```

On macOS/Linux use `.venv/bin/python` instead of `.venv\Scripts\python.exe`.

**With pip (with venv activated):**

```bash
pip install -r requirements.txt
```

---

## 5. Environment Variables

The app reads configuration from a `.env` file in the **repository root** (one level above `Sugar_Rehab_Companion`).

### 5.1. Create `.env`

In the project root (`Rehab-Coach-Bot`), create a file named `.env` (no extension).

### 5.2. Required variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | Used by the agents (OpenAI API). Get a key from [platform.openai.com](https://platform.openai.com/api-keys). |
| `PUSHOVER_API_TOKEN` | Application API token for coach push notifications. |
| `PUSHOVER_USER_KEY` | Recipient coach’s Pushover user or group key. |
| `PUSHOVER_DEVICE` | Optional device name; omit to notify all recipient devices. |

Example `.env` (use your own keys):

```env
OPENAI_API_KEY=sk-your-openai-key-here
PUSHOVER_API_TOKEN=your-application-token
PUSHOVER_USER_KEY=your-coach-user-key
# PUSHOVER_DEVICE=your-device-name
```

Do not commit `.env` or share these keys; `.env` should already be in `.gitignore`.

---

## 6. Run the App

### 6.1. From the Sugar_Rehab_Companion folder

Make sure you’re in `Sugar_Rehab_Companion` and that the virtual environment is activated (see 4.3).

### 6.2. Launch the Gradio UI (recommended)

```bash
python chat_window.py
```

This starts a local Gradio server and should open the “Sugar Rehab Companion” interface in your browser. If it doesn’t, open the URL shown in the terminal (e.g. `http://127.0.0.1:7860`).

### 6.3. Run without the UI (optional)

If you only want to use the companion logic (e.g. from another script), you can import and use `SugarRehabCompanion` from `sugar_rehab_companion.py`; the main entry point for the interactive app is `chat_window.py`.

---

## 7. IDE / Editor Setup (Optional)

For correct import resolution and IntelliSense (e.g. “Import gradio could not be resolved”):

- **VS Code / Cursor:** the repo includes `.vscode/settings.json` pointing the default Python interpreter to `Sugar_Rehab_Companion/.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (adjust path on macOS/Linux if needed).
- Or use **Python: Select Interpreter** from the Command Palette and choose the interpreter inside `Sugar_Rehab_Companion/.venv`.

---

## Quick Reference

| Step | Command (Windows, from repo root) |
|------|-----------------------------------|
| Go to app folder | `cd Sugar_Rehab_Companion` |
| Create venv | `uv venv` |
| Activate venv | `.\.venv\Scripts\activate` |
| Install deps | `uv pip install -r requirements.txt --python .venv\Scripts\python.exe` |
| Run app | `python chat_window.py` |

Ensure `.env` exists in the repo root with at least `OPENAI_API_KEY` set before running.

## Pushover coach notifications

**Current routing:** the moderator hands off to the Coach Notification Agent,
which attempts both Resend email and Pushover on every escalation.
Set `RESEND_API_KEY` in the root `.env` and restart the app. Emails use
`onboarding@resend.dev` and the fixed recipient `willowsayswhat@gmail.com`.
Check the app console for the Resend email ID or rejection details.
Configure the Pushover credentials below as well. Both channels are attempted
independently, and each result is logged. A failed channel does not prevent the other.

1. Install Pushover on the coach’s phone and sign in.
2. [Register a Pushover application](https://pushover.net/apps/build) and copy its API token into `PUSHOVER_API_TOKEN` in the root `.env`.
3. Copy the recipient’s user key from their [Pushover dashboard](https://pushover.net/) into `PUSHOVER_USER_KEY`.
4. Optionally set `PUSHOVER_DEVICE` to a registered device name. Restart the app after editing `.env`.

The combined notification tool uses the Pushover settings above. Missing Pushover credentials produce a notification failure result; they do not trigger an email fallback.

The sender follows the [Pushover Message API](https://pushover.net/api): plain-text titles up to 250 characters and messages up to 1024 characters. Requests time out after 10 seconds. A successful API response confirms acceptance, not that the coach has read the alert. Each moderation run permits one delivery attempt; a later chat message may trigger another alert. Failed or uncertain deliveries are not automatically retried.

To send a manual test alert from `Sugar_Rehab_Companion` with your virtual environment active:

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); from pushover_client import send_push_notification; print(send_push_notification('Rehab Coach test', 'Pushover notifications are configured.'))"
```

This command sends a real notification to the configured recipient.
## Next.js chat

Use Python with the existing coach credentials and Node.js 22. Set a long random
`COACH_API_TOKEN` in the environment of both servers. For local development,
put it in the repository root `.env` for Python and in `frontend/.env.local`
for Next.js. Add `COACH_API_URL=http://127.0.0.1:8000` to `frontend/.env.local`.

From the repository root, start the Python API:

```sh
python -m pip install -r Sugar_Rehab_Companion/requirements.txt
python -m uvicorn app:app --app-dir Sugar_Rehab_Companion
```

In another terminal, start the frontend:

```sh
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. The transcript lives in the current page and the
coach receives one message at a time.

### Vercel setup

1. Import this repository as a FastAPI project with `Sugar_Rehab_Companion` as
   its root directory. Set `OPENAI_API_KEY`, `COACH_API_TOKEN`, and the coach
   notification credentials on this project.
2. Import the same repository as a Next.js project with `frontend` as its root
   directory. Set `COACH_API_URL` to the deployed Python API origin and set
   `COACH_API_TOKEN` to the same value as the API project.
3. Restrict access to the frontend preview while developing sign-in. The
   shared token authenticates Next.js to Python. Anyone who can access the
   frontend can call its chat route, which runs the coach and may send alerts.

If the FastAPI preview uses Vercel Authentication, create a **Protection Bypass
for Automation** secret in the FastAPI project's **Settings → Deployment
Protection**. Add it to the Next.js project's Preview environment as
`COACH_API_VERCEL_BYPASS_SECRET` and redeploy the frontend. Next.js sends it
as a separate header alongside the existing `COACH_API_TOKEN`.
