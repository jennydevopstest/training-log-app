import json
import os
import uuid
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("workouts", __name__)

DATA_PATH = os.path.join("data", "workouts.json")


def _load_workouts():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_workouts(workouts):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(workouts, f, ensure_ascii=False, indent=2)


@bp.get("/")
def index():
    workouts = _load_workouts()
    workouts = sorted(workouts, key=lambda w: w["workout_date"], reverse=True)
    return render_template("index.html", workouts=workouts)


@bp.get("/workouts/new")
def new_workout():
    return render_template("new_workout.html", today=date.today().isoformat())


@bp.post("/workouts")
def create_workout():
    title = request.form.get("title", "").strip()
    workout_date = request.form.get("workout_date", "").strip()
    duration_min = request.form.get("duration_min", "").strip()
    notes = request.form.get("notes", "").strip()

    if not title:
        flash("Titel krävs.", "error")
        return redirect(url_for("workouts.new_workout"))

    if not workout_date:
        workout_date = date.today().isoformat()

    try:
        duration_min_int = int(duration_min) if duration_min else None
    except ValueError:
        flash("Duration måste vara ett heltal (minuter).", "error")
        return redirect(url_for("workouts.new_workout"))

    workouts = _load_workouts()

    workout = {
        "id": str(uuid.uuid4()),
        "title": title,
        "workout_date": workout_date,
        "duration_min": duration_min_int,
        "notes": notes,
    }

    workouts.append(workout)
    _save_workouts(workouts)

    flash("Träningspass sparat!", "success")
    return redirect(url_for("workouts.index"))


@bp.get("/workouts/<workout_id>")
def workout_detail(workout_id):
    workouts = _load_workouts()
    workout = next((w for w in workouts if w["id"] == workout_id), None)
    if not workout:
        flash("Hittade inte passet.", "error")
        return redirect(url_for("workouts.index"))

    return render_template("workout_detail.html", workout=workout)