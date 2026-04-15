# Nology Cashback

Aplicação fullstack para o desafio de cashback com:
- API em FastAPI (Python)
- Persistência em PostgreSQL
- Frontend estatico em HTML/CSS/JS puro

## Arquitetura
- Backend: `backend/app`
- Frontend: `frontend`

## Regras de cashback implementadas
1. Cashback base: 5% sobre o valor final da compra (apos desconto).
2. Compras com valor final acima de R$ 500 recebem multiplicador de 2 sobre o cashback base.
3. Cliente VIP recebe bonus adicional de 10% sobre o cashback base, calculado depois da dobra.
4. Ordem aplicada: base -> multiplicador >500 -> bonus VIP.

## Execucao local
### 1) Subir Postgres
```bash
docker compose up -d
```

### 2) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Rodar API:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs:
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### 3) Frontend estatico
```bash
cd frontend
python -m http.server 5500
```

Abrir no navegador:
- http://127.0.0.1:5500

## Endpoints
- `POST /api/v1/cashback/calculate`
  - Body:
```json
{
  "customer_type": "vip",
  "purchase_amount": 600,
  "discount_percent": 15
}
```
- `GET /api/v1/cashback/history`
  - Retorna apenas o historico do IP da requisicao.

## Testes
```bash
cd backend
source .venv/bin/activate
pytest -q
```

## Aplicação em produção
- Frontend publicado em: https://cashback-app-nine.vercel.app/
- A API de producao é consumida diretamente pelo frontend.

### Observação sobre o frontend
- O frontend usa a URL configurada em `frontend/config.js` para chamar a API.
- Em desenvolvimento local, ele continua apontando para o backend local quando nao houver configuracao explicita.

## Observações
- Para facilitar desenvolvimento local, o app cria tabelas automaticamente no startup.
- Em produção, prefira usar apenas migracoes Alembic.
