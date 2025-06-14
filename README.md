Absolutely! Here's the complete, cleaned, and decorated `README.md` in a single block — ready for copy-paste:

---

````markdown
# 🧠✨ Code Documentation Generator (LLM + Novita.ai)

This project uses **Python + FastAPI** with a **Novita.ai-powered LLM** to generate high-quality inline code comments and documentation from pasted or uploaded code.

> 🚀 Ideal for developers building AI assistants, internal tools, or automated doc generators.

---

### 🐍 Create & Activate a Virtual Environment

#### 💻 Windows (Command Prompt)

```bash
python -m venv venv
venv\Scripts\activate
```

#### 🪟 Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 🐧 Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

> 💡 Tip: Make sure you're inside the virtual environment before running this.

---

### 🔐 Add Environment Variables

Create a `.env` file in the `/backend` directory:

```env
NOVITA_API_KEY=your_novita_api_key_here
```

> 🛡️ Keep this file secure and **do not commit it to version control**.

---

### 🚀 Run the Application

#### 🏁 Basic Python Run:

```bash
python main.py
```

#### 💻 macOS/Linux Alternative:

```bash
uvicorn main:app --reload
```

## 🔍 Features

* ✅ Paste or upload code
* 🧠 Inline and function-level comments
* 📄 JSON-style documentation output
* 🌐 Ready to plug into web UI or dev tools

## 🤝 Contributing

Feel free to fork this project, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you'd like to change.

```

---

Let me know if you'd like a matching `.env.example`, `requirements.txt`, or frontend `README` too!
```
