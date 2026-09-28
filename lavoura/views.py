from rest_framework import viewsets
from .models import Talhao, Lote
from .serializers import TalhaoSerializer, LoteSerializer

class TalhaoViewSet(viewsets.ModelViewSet):
    queryset = Talhao.objects.all()
    serializer_class = TalhaoSerializer


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.select_related('talhao').all()
    serializer_class = LoteSerializer
