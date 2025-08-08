# nlp_processor.py
# Lightweight intent detection using keyword rules + spaCy for simple extraction
import re
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_email(text):
    m = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return m.group(0) if m else None

def analyze_intent(text):
    t = text.lower()
    doc = nlp(text)

    # default
    result = {"intent": "unknown", "entities": {}}

    # greetings
    if any(w in t for w in ["hello", "hi", "hey", "good morning", "good evening"]):
        result["intent"] = "greet"
        return result

    if "time" in t:
        result["intent"] = "time"
        return result

    if "date" in t:
        result["intent"] = "date"
        return result

    if t.startswith("search") or "search for" in t:
        q = t.replace("search for", "").replace("search", "").strip()
        result["intent"] = "search"
        result["entities"]["query"] = q
        return result

    if "weather" in t:
        # try to extract location (proper nouns, GPE)
        loc = None
        for ent in doc.ents:
            if ent.label_ in ("GPE", "LOC"):
                loc = ent.text
                break
        result["intent"] = "weather"
        result["entities"]["location"] = loc
        return result

    if any(w in t for w in ["send email", "send an email", "email to", "send mail"]):
        email = extract_email(text)
        # naive subject/body extraction
        result["intent"] = "send_email"
        result["entities"]["email_to"] = email
        # you can extend to parse subject/body by pattern or prompting user
        return result

    if any(w in t for w in ["remind me", "set reminder", "reminder"]):
        # naive: if user says "remind me to call mom at 6pm"
        # capture title and time with heuristics
        result["intent"] = "set_reminder"
        # find time expressions using spaCy DATE/TIME entities
        for ent in doc.ents:
            if ent.label_ in ("TIME", "DATE"):
                result["entities"]["datetime"] = ent.text
                break
        # title fallback
        result["entities"]["title"] = t
        return result

    if any(w in t for w in ["list reminders", "show reminders", "my reminders"]):
        result["intent"] = "list_reminders"
        return result

    return result
