from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash

from .workouts_service import (
    load_workouts,
    save_workouts,
    get_workout_date,
    build_workout_from_form,
    find_workout_by_id,
)

bp = Blueprint("workouts", __name__)


@bp.get("/")
def index():
    workouts = load_workouts()
    workouts = sorted(workouts, key=get_workout_date, reverse=True)
    return render_template("index.html", workouts=workouts)


@bp.get("/workouts/new")
def new_workout():
    return render_template("new_workout.html", today=date.today().isoformat())


@bp.post("/workouts")
def create_workout():
    workout, error = build_workout_from_form(request.form)

    if error:
        flash(error, "error")
        return redirect(url_for("workouts.new_workout"))

    workouts = load_workouts()
    workouts.append(workout)
    save_workouts(workouts)

    flash("Träningspass sparat:", "success")
    return redirect(url_for("workouts.index"))


@bp.get("/workouts/<workout_id>")
def workout_detail(workout_id):
    workouts = load_workouts()
    workout = find_workout_by_id(workouts, workout_id)

    if not workout:
        flash("Hittade inte passet.", "error")
        return redirect(url_for("workouts.index"))

    return render_template("workout_detail.html", workout=workout)