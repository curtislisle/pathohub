from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from miqa.core.models import ScanNote

from .permissions import UserHoldsSessionLock, ensure_session_lock


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ScanNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanNote
        fields = ['id', 'initials', 'creator', 'note', 'created', 'modified']

    # Override the default DateTimeFields to disable read_only=True
    created = serializers.DateTimeField()
    modified = serializers.DateTimeField()

    creator = UserSerializer()


class CreateScanNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanNote
        fields = ['scan', 'note']


def user_initials(user):
    return f'{user.first_name[:1] or "?"}{user.last_name[:1] or "?"}'


class ScanNoteViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ScanNote.objects.select_related('scan__experiment__session')

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['scan', 'initials', 'creator']

    permission_classes = [IsAuthenticated, UserHoldsSessionLock]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateScanNoteSerializer
        return ScanNoteSerializer

    def perform_create(self, serializer: CreateScanNoteSerializer):
        user = self.request.user
        ensure_session_lock(serializer.validated_data['scan'], user)
        serializer.save(creator=user, initials=user_initials(user))
