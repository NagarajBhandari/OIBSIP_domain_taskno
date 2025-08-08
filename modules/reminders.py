# reminders.py
import uuid
import datetime

class ReminderManager:
    def __init__(self):
        self.reminders = {}  # id -> {title, datetime, created}

    def add_reminder(self, title, when_text):
        # naive: store human text; you can add parsing to datetime
        rid = str(uuid.uuid4())[:8]
        self.reminders[rid] = {
            "title": title,
            "when_text": when_text or "unspecified",
            "created": datetime.datetime.now().isoformat()
        }
        return f"{title} at {self.reminders[rid]['when_text']} (id {rid})"

    def list_reminders(self):
        if not self.reminders:
            return "You have no reminders."
        out = []
        for rid, r in self.reminders.items():
            out.append(f"{r['title']} — {r['when_text']} (id {rid})")
        return "\n".join(out)

    def remove_reminder(self, rid):
        return self.reminders.pop(rid, None)
