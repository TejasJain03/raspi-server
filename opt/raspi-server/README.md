## Quick Start

1) Create & activate virtualenv (optional)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2) Install deps
```bash
pip install -r requirements.txt
```

3) Run in dev with auto-reload
```bash
# using Flask CLI (recommended)
flask --app wsgi:app run --debug --port 5000
```
