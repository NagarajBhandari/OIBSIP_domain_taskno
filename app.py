from flask import Flask, render_template, request, jsonify
from modules.nlp_processor import analyze_intent
from modules.weather import get_weather_summary
from modules.email_sender import send_email
from modules.reminders import ReminderManager
from modules.speech_engine import speak_text
import webbrowser
import datetime
import config

app = Flask(__name__, static_folder="static", template_folder="templates")
reminders = ReminderManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"success": False, "response": "No input received."})

    # NLP: get intent and entities
    intent_data = analyze_intent(text)
    intent = intent_data.get("intent")
    entities = intent_data.get("entities", {})

    # simple intent handling
    if intent == "greet":
        resp = "Hello! How can I assist you today?"

    elif intent == "time":
        now = datetime.datetime.now()
        resp = f"The current time is {now.strftime('%I:%M %p')}."

    elif intent == "date":
        resp = f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}."

    elif intent == "search":
        q = entities.get("query") or text.replace("search", "").strip()
        if q:
            url = f"https://www.google.com/search?q={q.replace(' ', '+')}"
            # Optionally open on server machine:
            # webbrowser.open(url)
            resp = f"I searched the web for: {q}. (I can open it on the server if you want.)"
        else:
            resp = "What would you like me to search for?"

    elif intent == "weather":
        place = entities.get("location") or "your location"
        weather = get_weather_summary(place, api_key=config.OPENWEATHERMAP_API_KEY)
        resp = weather

    elif intent == "send_email":
        to = entities.get("email_to")
        subject = entities.get("subject") or "No subject"
        body = entities.get("body") or text
        if not to:
            resp = "Who should I send the email to? Please provide an email address."
        else:
            ok, err = send_email(to, subject, body,
                                 host=config.EMAIL_HOST, port=config.EMAIL_PORT,
                                 username=config.EMAIL_USER, password=config.EMAIL_PASS)
            resp = "Email sent successfully." if ok else f"Failed to send email: {err}"

    elif intent == "set_reminder":
        title = entities.get("title") or "Reminder"
        when = entities.get("datetime")  # naive: expected ISO or human text — see module
        r = reminders.add_reminder(title, when)
        resp = f"Reminder set: {r}" if r else "Could not set reminder. Please provide a time."

    elif intent == "list_reminders":
        resp = reminders.list_reminders()

    else:
        # fallback: echo/search
        resp = "I didn't quite get that. I can tell time, date, weather, send email, set reminders, or search the web."

    # optional: speak response on server speaker
    try:
        # comment out if running on headless server
        speak_text(resp)
    except Exception:
        pass

    return jsonify({"success": True, "response": resp, "intent": intent, "entities": entities})

if __name__ == "__main__":
    app.run(debug=True)
