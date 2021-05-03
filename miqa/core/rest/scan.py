from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from miqa.core.models import Scan


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['id', 'scan_id', 'scan_type', 'note', 'decision', 'experiment', 'site']

    decision = serializers.ChoiceField(choices=Scan.decision.field.choices)


class ScanViewSet(ReadOnlyModelViewSet):
    queryset = Scan.objects.all()

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['experiment', 'site']

    permission_classes = [AllowAny]
    serializer_class = ScanSerializer