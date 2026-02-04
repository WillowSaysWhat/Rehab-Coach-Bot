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
| `SENDGRID_API_KEY` | Used for email alerts (SendGrid). Optional if you don’t need coach email notifications. Get a key from [SendGrid](https://sendgrid.com/). |

Example `.env` (use your own keys):

```env
OPENAI_API_KEY=sk-your-openai-key-here
SENDGRID_API_KEY=SG.your-sendgrid-key-here
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
