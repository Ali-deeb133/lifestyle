from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import BodyProfile
from .serializers import BodyProfileSerializer


class BodyProfileCreateView(generics.CreateAPIView):

    serializer_class = BodyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        warnings = getattr(serializer, "_warnings", [])

        return Response(
            {
                "status": "warning" if warnings else "success",
                "warnings": warnings,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

# Last Input
class LatestBodyProfileView(generics.RetrieveAPIView):

    serializer_class = BodyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return BodyProfile.objects.filter(
            user=self.request.user
        ).order_by("-created_at").first()