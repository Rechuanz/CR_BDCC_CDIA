from django.db import models

class Talhao(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('em_colheita', 'Em colheita'),
    ]

    nome = models.CharField(max_length=200)
    produtor = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    cultura = models.CharField(max_length=100)
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2)
    umidade_solo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ph_solo = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    temperatura_solo = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    geojson = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    imagem = models.ImageField(upload_to='talhoes/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Lote(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    talhao = models.ForeignKey(Talhao, on_delete=models.CASCADE, related_name='lotes')
    codigo = models.CharField(max_length=50, unique=True)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    motivo = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo
