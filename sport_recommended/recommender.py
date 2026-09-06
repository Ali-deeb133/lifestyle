import joblib
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity

class FitnessRecommender:

    def __init__(self, bundle_path):
        self.bundle = joblib.load(bundle_path)

        self.program_vectors = self.bundle["program_vectors"]
        self.program_df = self.bundle["program_df"]
        self.exercise_df = self.bundle["exercise_df"]

        self.tfidf = self.bundle["tfidf"]
        self.ohe = self.bundle["equipment_ohe"]
        self.scaler = self.bundle["length_scaler"]

    # Build User Vector (Weighted Features)
    def _build_user_vector(
        self,
        level,
        goal,
        equipment,
        program_length
    ):
        level_text = " ".join(level) if level else ""
        goal_text = " ".join(goal) if goal else ""

        text = f"{level_text} {goal_text}"

        text_vec = self.tfidf.transform([text]) * 2.0
        equip_vec = self.ohe.transform([[equipment]]) * 1.5
        length_vec = self.scaler.transform([[program_length]]) * 1.5

        return hstack([text_vec, equip_vec, length_vec])

    # Recommendation
    def recommend(
        self,
        level,
        goal,
        equipment,
        program_length,
        min_weeks=8,
        max_weeks=12,
        top_n=5
    ):

        # User Vector
        user_vec = self._build_user_vector(
            level, goal, equipment, program_length
        )

        # Cosine Similarity
        similarities = cosine_similarity(
            user_vec, self.program_vectors
        )[0]

        df = self.program_df.copy()
        df["similarity"] = similarities

        # Length Filter
        df = df[
            (df["program_length"] >= min_weeks) &
            (df["program_length"] <= max_weeks)
        ]

        # Level Compatibility Filter
        def level_match(program_levels):
            return any(l in program_levels for l in level)

        df = df[df["level"].apply(level_match)]

        # Rule-based Boosting
        df["boost"] = 0.0

        df.loc[
            df["equipment"] == equipment,
            "boost"
        ] += 0.1

        df.loc[
            df["level"].apply(lambda x: any(l in x for l in level)),
            "boost"
        ] += 0.15

        df.loc[
            df["goal"].apply(lambda x: any(g in x for g in goal)),
            "boost"
        ] += 0.2

        df["final_score"] = df["similarity"] + df["boost"]

        # Sort & Select
        top_programs = (
            df
            .sort_values("final_score", ascending=False)
            .head(top_n)
        )

        # Attach Exercises
        results = []

        for _, row in top_programs.iterrows():
            exercises = self.exercise_df[
                self.exercise_df["title"] == row["title"]
            ][[
                "week",
                "day",
                "exercise_name",
                "sets",
                "reps_display",
                "number_of_exercises"
            ]]

            results.append({
                "title": row["title"],
                "description": row["description"],
                "level": row["level"],
                "goal": row["goal"],
                "program_length": int(row["program_length"]),
                "total_exercises": int(row["total_exercises"]),
                "time_per_workout": row["time_per_workout"],
                "similarity": round(float(row["final_score"]), 4),
                "exercises": exercises.to_dict("records")
            })

        return results