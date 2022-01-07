from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from miqa.core.models.scan_decision import ArtifactState, default_identified_artifacts


class MIQAConfigView(APIView):
    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def get(self, request):
        return Response(
            {
                'artifact_options': [key for key in default_identified_artifacts()],
                'auto_artifact_threshold': 0.4,
                'artifact_states': {
                    'PRESENT': ArtifactState.PRESENT.value,
                    'ABSENT': ArtifactState.ABSENT.value,
                    'UNDEFINED': ArtifactState.UNDEFINED.value,
                },
            }
        )