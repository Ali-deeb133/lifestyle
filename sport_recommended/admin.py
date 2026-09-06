from django.contrib import admin
from .models import Level, Goal, TrainingProgram, ProgramExercise, RecommendationRequest, RecommendedProgram

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    search_fields = ("name",)

class ProgramExerciseInline(admin.TabularInline):
    model = ProgramExercise
    extra = 0

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "get_levels", "get_goals", "equipment", "program_length")
    list_filter = ("levels", "goals", "equipment")
    search_fields = ("title", "description")
    inlines = [ProgramExerciseInline]

    def get_levels(self, obj):
        return ", ".join([l.name for l in obj.levels.all()])
    get_levels.short_description = "Levels"

    def get_goals(self, obj):
        return ", ".join([g.name for g in obj.goals.all()])
    get_goals.short_description = "Goals"

@admin.register(RecommendationRequest)
class RecommendationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "goal", "equipment", "program_length", "created_at")
    list_filter = ("level", "goal", "equipment")

@admin.register(RecommendedProgram)
class RecommendedProgramAdmin(admin.ModelAdmin):
    list_display = ("request", "program", "similarity_score")