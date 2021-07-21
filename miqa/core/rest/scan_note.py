from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet

from miqa.core.models import ScanNote


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


class ScanNoteViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ScanNote.objects.all()

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['scan', 'initials', 'creator']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateScanNoteSerializer
        return ScanNoteSerializer

    def perform_create(self, serializer: CreateScanNoteSerializer):
        user = self.request.user

        def initial(name):
            if name:
                return name[0]
            return '?'

        note = ScanNote(
            **serializer.validated_data,
            creator=user,
            initials=f'{initial(user.first_name)}{initial(user.last_name)}',
        )
        note.save()
