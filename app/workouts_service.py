import json
import os
import uuid
from datetime import date

DATA_PATH = os.path.join("data", "workouts.json")


def load_workouts():
    file_exists = os.path.exists(DATA_PATH)

    if file_exists == False:
        workouts = []
        return workouts
    else:
        f = open(DATA_PATH, "r", encoding="utf-8")
        file_contents = f.read()
        f.close()

        workouts = json.loads(file_contents)
        return workouts


def save_workouts(workouts):
    folder_path = os.path.dirname(DATA_PATH)
    folder_exists = os.path.exists(folder_path)

    if folder_exists == False:
        os.makedirs(folder_path)

    f = open(DATA_PATH, "w", encoding="utf-8")
    json_text = json.dumps(workouts, ensure_ascii=False, indent=2)
    f.write(json_text)
    f.close()


def get_workout_date(workout):
    return workout["workout_date"]


def build_workout_from_form(form):
    title = form.get("title", "").strip()
    workout_date = form.get("workout_date", "").strip()
    duration_min = form.get("duration_min", "").strip()
    notes = form.get("notes", "").strip()

    if not title:
        return None, "Titel krävs."

    if not workout_date:
        workout_date = date.today().isoformat()

    try:
        duration_min_int = int(duration_min) if duration_min else None
    except ValueError:
        return None, "Duration måste vara ett heltal (minuter)."

    workout = {
        "id": str(uuid.uuid4()),
        "title": title,
        "workout_date": workout_date,
        "duration_min": duration_min_int,
        "notes": notes,
    }
    return workout, None


def find_workout_by_id(workouts, workout_id):
    workout = next((w for w in workouts if w["id"] == workout_id), None)
    return workout