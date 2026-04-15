# Nology Cashback

Aplicacao fullstack para o desafio de cashback com:
- API em FastAPI (Python)
- Persistencia em PostgreSQL
- Frontend estatico em HTML/CSS/JS puro

## Arquitetura
- Backend: `backend/app`
- Frontend: `frontend`
- Respostas das questoes 2-4: `docs/respostas_desafio.md`

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

## Deploy sugerido
- Backend + PostgreSQL: Railway
- Frontend estatico: Vercel

### Variaveis de ambiente no backend (Railway)
- `DATABASE_URL`
- `FRONTEND_ORIGIN` (URL final do frontend)

### Passos de deploy
1. Suba o backend no Railway apontando para `backend/` como raiz do projeto.
2. Configure no Railway as variaveis `DATABASE_URL` e `FRONTEND_ORIGIN` com a URL publica do Vercel.
3. Use o start command do `backend/Procfile` ou equivalente: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Publique o frontend no Vercel a partir da pasta `frontend/`.
5. Atualize `frontend/config.js` com a URL publica da API do Railway antes do deploy do frontend.
6. Teste no navegador os endpoints `POST /api/v1/cashback/calculate` e `GET /api/v1/cashback/history`.

### Observacao sobre o frontend
- O frontend tenta usar `frontend/config.js` primeiro.
- Se a URL nao estiver configurada, ele usa automaticamente o backend local em desenvolvimento.

## Observacoes
- Para facilitar desenvolvimento local, o app cria tabelas automaticamente no startup.
- Em producao, prefira usar apenas migracoes Alembic.
