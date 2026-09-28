# Lavoura Inteligente

API REST para o monitoramento de talhões agrícolas e do rastreio dos lotes colhidos em cada um deles. O projeto registra dados de solo (umidade, pH e temperatura), a área e a cultura de cada talhão, o polígono no formato GeoJSON, e controla o peso e a situação de cada lote produzido.

## O que é a Lavoura Inteligente

Um produtor rural precisa saber o que acontece em cada parte da propriedade. A Lavoura Inteligente organiza essa informação em dois conceitos:

- **Talhão**: uma área da lavoura, com produtor, cultura plantada, tamanho em hectares, leituras do solo e geometria no mapa.
- **Lote**: uma quantidade colhida de um talhão, identificada por um código único, com peso em quilos, status e motivo (por exemplo, o motivo de uma rejeição).

Todo o acesso é feito por uma API JSON, criada com Django REST Framework, que também expõe a interface navegável do DRF e o painel `/admin/`.

## Este repositório: projeto preparado para deploy em Elastic Beanstalk

Este é um projeto reduzido, pensado para praticar o deploy de uma aplicação Django no AWS Elastic Beanstalk. Ele tem apenas a API, o banco SQLite e a configuração de deploy, sem front-end.

## Estrutura do projeto

```
DeployEB/
├── .ebextensions/
│   ├── django.config        # WSGIPath, variáveis de ambiente, migrate e collectstatic
│   └── detection.config
├── .elasticbeanstalk/
│   └── config.yml           # configuração da aplicação no EB CLI
├── lavoura_inteligente/     # projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── lavoura/                 # app com os models e a API
│   ├── models.py            # Talhao e Lote
│   ├── serializers.py
│   ├── views.py             # ModelViewSets
│   ├── urls.py              # rotas /api/talhoes/ e /api/lotes/
│   ├── admin.py
│   └── migrations/
├── media/talhoes/           # imagens enviadas dos talhões
├── manage.py
├── Procfile                 # gunicorn lavoura_inteligente.wsgi
└── requirements.txt
```

## Modelo de dados

```
Talhao 1 ────── N Lote
```

Um talhão pode ter vários lotes. Ao apagar um talhão, os lotes dele também são apagados.

### Talhao

| Campo | Tipo | Observação |
|---|---|---|
| nome | CharField | |
| produtor | CharField | |
| descricao | TextField | opcional |
| cultura | CharField | ex.: soja, milho |
| area_hectares | DecimalField | |
| umidade_solo | DecimalField | opcional |
| ph_solo | DecimalField | opcional |
| temperatura_solo | DecimalField | opcional |
| geojson | JSONField | opcional, polígono do talhão |
| status | CharField | `ativo`, `inativo` ou `em_colheita` |
| imagem | ImageField | opcional, salva em `media/talhoes/` |
| data_criacao | DateTimeField | preenchido automaticamente |

### Lote

| Campo | Tipo | Observação |
|---|---|---|
| talhao | ForeignKey | referência ao `Talhao` |
| codigo | CharField | único |
| peso_kg | DecimalField | |
| status | CharField | `pendente`, `aprovado` ou `rejeitado` |
| motivo | TextField | opcional |
| data_criacao | DateTimeField | preenchido automaticamente |

## Endpoints

| Método | Rota | Ação |
|---|---|---|
| GET, POST | `/api/talhoes/` | listar e criar talhões |
| GET, PUT, PATCH, DELETE | `/api/talhoes/{id}/` | detalhar, alterar e remover um talhão |
| GET, POST | `/api/lotes/` | listar e criar lotes |
| GET, PUT, PATCH, DELETE | `/api/lotes/{id}/` | detalhar, alterar e remover um lote |
| GET | `/` | health check do Elastic Beanstalk |
| | `/admin/` | painel administrativo do Django |

## Stack

- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite
- Pillow (upload de imagens)
- Gunicorn
- AWS Elastic Beanstalk

## Rodando localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # opcional, para acessar o /admin/
python manage.py runserver
```

A API fica em `http://127.0.0.1:8000/api/`.

Exemplo de criação de um talhão:

```bash
curl -X POST http://127.0.0.1:8000/api/talhoes/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Talhão 1", "produtor": "Fazenda Boa Vista", "cultura": "Soja", "area_hectares": "12.50"}'
```

## Deploy no Elastic Beanstalk

A configuração de deploy já está pronta em `.ebextensions/django.config`. Ela aponta o `WSGIPath` para `lavoura_inteligente/wsgi.py`, define `DJANGO_SETTINGS_MODULE` e roda `migrate` e `collectstatic` a cada deploy.

```bash
eb init
eb create
eb deploy
```

O `DJANGO_DEBUG` fica `False` no Elastic Beanstalk. Para liberar outros domínios, defina a variável `DJANGO_ALLOWED_HOSTS` no ambiente.
