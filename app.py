import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, url_for

from config import load_settings
from services.ai_service import DeepSeekHealthAdvisor


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
PROMPT_FILE = BASE_DIR / "prompts" / "health_advisor_zh.md"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("ai-health-demo")

settings = load_settings()
app = Flask(
    __name__,
    static_url_path="/static",
    static_folder=str(BASE_DIR / "static"),
)
advisor = DeepSeekHealthAdvisor(settings=settings, prompt_file=PROMPT_FILE)


def _feature_cards():
    return [
        {
            "title": "Stress & Mood Support",
            "description": "Identify stress patterns and receive practical coping strategies for daily life.",
            "icon": url_for("static", filename="images/icon_stress.png"),
        },
        {
            "title": "Sleep Improvement",
            "description": "Get actionable sleep hygiene suggestions based on your routines and symptoms.",
            "icon": url_for("static", filename="images/icon_sleep.png"),
        },
        {
            "title": "Nutrition Guidance",
            "description": "Receive balanced, realistic diet recommendations adapted to your context.",
            "icon": url_for("static", filename="images/icon_diet.png"),
        },
        {
            "title": "Activity Planning",
            "description": "Build sustainable movement habits with intensity and duration guidance.",
            "icon": url_for("static", filename="images/icon_exercise.png"),
        },
    ]


def _validate_user_input(payload: dict) -> Tuple[bool, str]:
    user_input = str(payload.get("userInput", "")).strip()
    if not user_input:
        return False, "Missing userInput."
    if len(user_input) > settings.max_input_chars:
        return False, f"userInput is too long. Max {settings.max_input_chars} characters."
    return True, user_input


@app.context_processor
def inject_global_template_vars():
    return {"current_year": datetime.now().year}


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "ai_ready": advisor.is_ready,
            "model": settings.deepseek_model,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/")
def index():
    return render_template("index.html", features=_feature_cards())


@app.post("/process")
@app.post("/api/process")
def process_data():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json(silent=True) or {}
    is_valid, result = _validate_user_input(payload)
    if not is_valid:
        return jsonify({"error": result}), 400

    try:
        ai_result = advisor.generate_advice(result)
        return jsonify({"result": ai_result})
    except RuntimeError as exc:
        logger.warning("AI client unavailable: %s", exc)
        return jsonify({"error": "AI service is not configured on the server."}), 503
    except Exception:
        logger.exception("Unexpected error while calling AI service.")
        return jsonify({"error": "AI service is temporarily unavailable."}), 503


@app.get("/about")
def about_page():
    return render_template("about.html")


@app.get("/team")
def team_page():
    return render_template("team.html")


@app.get("/how-it-works")
def how_it_works_page():
    return render_template("how_it_works.html")


@app.get("/features")
def features_page():
    return render_template("features.html", features=_feature_cards())


@app.get("/contact")
def contact_page():
    return render_template("contact.html")


if __name__ == "__main__":
    logger.info(
        "Starting app on %s:%s (debug=%s, ai_ready=%s)",
        settings.flask_host,
        settings.flask_port,
        settings.flask_debug,
        advisor.is_ready,
    )
    app.run(
        debug=settings.flask_debug,
        host=settings.flask_host,
        port=settings.flask_port,
    )
