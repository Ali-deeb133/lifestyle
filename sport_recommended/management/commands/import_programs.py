import csv, ast, os
from django.core.management.base import BaseCommand
from django.conf import settings
from sport_recommended.models import TrainingProgram, ProgramExercise, Level, Goal

class Command(BaseCommand):
    help = "Import Training Programs and Exercises"

    def handle(self, *args, **kwargs):
        programs_path = os.path.join(settings.BASE_DIR, "sport_recommended", "data", "clean_sampled_programs.csv")
        exercises_path = os.path.join(settings.BASE_DIR, "sport_recommended", "data", "clean_sampled_exercises.csv")

        # Import programs
        with open(programs_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                obj, _ = TrainingProgram.objects.update_or_create(
                    title=row["title"],
                    defaults={
                        "description": row["description"],
                        "equipment": row["equipment"],
                        "program_length": int(float(row["program_length"])),
                        "time_per_workout": row["time_per_workout"],
                        "total_exercises": int(float(row["total_exercises"])),
                    }
                )

                # Levels & Goals
                obj.levels.clear()
                obj.goals.clear()
                levels = ast.literal_eval(row["level"])
                goals = ast.literal_eval(row["goal"])
                for l in levels:
                    level_obj, _ = Level.objects.get_or_create(name=l.strip())
                    obj.levels.add(level_obj)
                for g in goals:
                    goal_obj, _ = Goal.objects.get_or_create(name=g.strip())
                    obj.goals.add(goal_obj)

        # Import exercises
        with open(exercises_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    program = TrainingProgram.objects.get(title=row["title"])
                    ProgramExercise.objects.create(
                        program=program,
                        week=int(float(row["week"])),
                        day=int(float(row["day"])),
                        number_of_exercises=int(float(row["number_of_exercises"])),
                        exercise_name=row["exercise_name"],
                        sets=row["sets"],
                        reps_display=row["reps_display"]
                    )
                except TrainingProgram.DoesNotExist:
                    print(f"Program not found: {row['title']}")