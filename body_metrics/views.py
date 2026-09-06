from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import BodyMetrics
from .serializers import BodyMetricsSerializer


class CalculateBodyMetricsView(generics.CreateAPIView):

    serializer_class = BodyMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        warnings = getattr(serializer, "_warnings", [])

        return Response(
            {
                "status": "warning" if warnings else "success",
                "warnings": warnings,
                "data": BodyMetricsSerializer(instance).data,
            },
            status=status.HTTP_201_CREATED
        )