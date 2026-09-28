from rest_framework import serializers
from .models import Talhao, Lote

class TalhaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talhao
        fields = ['id', 'nome', 'produtor', 'descricao', 'cultura', 'area_hectares',
                  'umidade_solo', 'ph_solo', 'temperatura_solo', 'geojson', 'status',
                  'imagem', 'data_criacao']


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ['id', 'talhao', 'codigo', 'peso_kg', 'status', 'motivo', 'data_criacao']
