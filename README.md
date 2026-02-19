# AI Health Demo (Refactored)

A Flask-based AI health lifestyle assistant demo that turns free-text input into structured, non-medical recommendations.

This version is heavily optimized from an older prototype with:
- cleaner backend architecture
- safer request handling
- configurable model/runtime settings
- fixed template issues and improved frontend behavior

## Highlights

- **Refactored backend**:
  - `config.py` for centralized environment configuration
  - `services/ai_service.py` for DeepSeek client abstraction
  - prompt moved to `prompts/health_advisor_zh.md` (no giant hardcoded string in `app.py`)
- **Operational safeguards**:
  - JSON and input-length validation
  - consistent 4xx/5xx API responses
  - `/health` endpoint for service readiness checks
- **Frontend quality fixes**:
  - mobile navigation toggle now works
  - keyboard shortcut (`Ctrl/Cmd + Enter`) to submit
  - markdown rendering fallback when CDN script is unavailable
- **Template cleanup**:
  - repaired broken `team.html` structure
  - normalized feature rendering using backend-provided cards

## Tech Stack

- Backend: Python, Flask
- AI service: DeepSeek API via OpenAI Python SDK
- Frontend: HTML, CSS, JavaScript (Jinja2 templates)
- Config: `.env` + `python-dotenv`

## Project Structure

```text
ai-health-demo/
├── app.py
├── config.py
├── services/
│   └── ai_service.py
├── prompts/
│   └── health_advisor_zh.md
├── templates/
├── static/
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start

1. Clone:
```bash
git clone https://github.com/Gatsby0916/ai-health-demo.git
cd ai-health-demo
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```
Then set:
```env
DEEPSEEK_API_KEY=your_real_key
```

5. Run:
```bash
python app.py
```
Open `http://127.0.0.1:5000`.

## API

### `POST /process`
Request:
```json
{
  "userInput": "I have been stressed and sleeping poorly for 2 weeks..."
}
```

Response:
```json
{
  "result": "..."
}
```

### `GET /health`
Returns service status and model readiness.

## Safety Notice

This project provides **non-medical lifestyle guidance only**.
It does **not** provide diagnosis, treatment plans, or medication advice.
For urgent or severe symptoms, users should seek licensed medical care immediately.

## Next Improvements (Suggested)

- add automated tests for route validation and service mocking
- add request rate limiting and basic telemetry
- add multilingual toggle (ZH/EN) for content rendering
- deploy with Docker and production WSGI configuration
