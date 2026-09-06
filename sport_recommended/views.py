from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializers import RecommendationInputSerializer
from .models import RecommendationRequest, RecommendedProgram, TrainingProgram, Level, Goal
from .recommender import FitnessRecommender

class RecommendProgramAPIView(APIView):
    def post(self, request):
        serializer = RecommendationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        model = FitnessRecommender(settings.RECOMMENDER_MODEL_PATH)

        # call ML model
        results = model.recommend(
            level=[data["level"]],
            goal=[data["goal"]],
            equipment=data["equipment"],
            program_length=data["program_length"]
        )

        # save RecommendationRequest
        level_obj = Level.objects.get(name=data["level"])
        goal_obj = Goal.objects.get(name=data["goal"])
        rec_request = RecommendationRequest.objects.create(
            user=request.user,
            level=level_obj,
            goal=goal_obj,
            equipment=data["equipment"],
            program_length=data["program_length"]
        )

        # save RecommendedProgram
        for item in results:
            program = TrainingProgram.objects.get(title=item["title"])
            RecommendedProgram.objects.create(
                request=rec_request,
                program=program,
                similarity_score=item["similarity"]
            )

        return Response(results)