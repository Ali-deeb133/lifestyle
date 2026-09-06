from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Level(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Goal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class TrainingProgram(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    levels = models.ManyToManyField(Level, related_name="programs")
    goals = models.ManyToManyField(Goal, related_name="programs")
    equipment = models.CharField(max_length=50)
    program_length = models.IntegerField()
    time_per_workout = models.CharField(max_length=100)
    total_exercises = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProgramExercise(models.Model):
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name="exercises")
    week = models.IntegerField()
    day = models.IntegerField()
    number_of_exercises = models.IntegerField()
    exercise_name = models.CharField(max_length=255)
    sets = models.CharField(max_length=50)
    reps_display = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.program.title} - Week {self.week} Day {self.day}"


class RecommendationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    equipment = models.CharField(max_length=50)
    program_length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class RecommendedProgram(models.Model):
    request = models.ForeignKey(RecommendationRequest, on_delete=models.CASCADE, related_name="results")
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
    similarity_score = models.FloatField()

    def __str__(self):
        return f"{self.program.title} - {self.similarity_score}"