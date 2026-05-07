# Cashback Simulator

Fullstack application for a cashback challenge featuring:
- **FastAPI** (Python) backend
- **PostgreSQL** persistence
- **Vanilla HTML/CSS/JS** static frontend

## Architecture

- Backend: `backend/app`
- Frontend: `frontend`

## Cashback Rules Implemented

1. **Base cashback:** 5% on the final purchase amount (after discount)
2. **Doubling rule:** Purchases with final amount above R$ 500 receive a 2x multiplier on the base cashback
3. **VIP bonus:** VIP customers receive an additional 10% bonus on the base cashback, calculated after the doubling
4. **Application order:** Base → Doubling (if > R$500) → VIP bonus

### Calculation Examples

| Purchase | Discount | Final | Customer | Base (5%) | Double? | VIP Bonus | Total Cashback |
|----------|----------|-------|----------|-----------|---------|-----------|----------------|
| R$ 100 | 0% | R$ 100 | Regular | R$ 5 | No | N/A | **R$ 5** |
| R$ 600 | 0% | R$ 600 | Regular | R$ 30 | Yes (2x → R$ 60) | N/A | **R$ 60** |
| R$ 600 | 0% | R$ 600 | VIP | R$ 30 | Yes (2x → R$ 60) | +10% of base (R$ 3) | **R$ 63** |
| R$ 1000 | 20% | R$ 800 | VIP | R$ 40 | Yes (2x → R$ 80) | +10% of base (R$ 4) | **R$ 84** |

## Local Development

### 1) Start PostgreSQL

```bash
docker compose up -d
```

### 2) Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API Documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

### 3) Static Frontend

```bash
cd frontend
python -m http.server 5500
```

Open in browser:

- http://127.0.0.1:5500

## API Endpoints

### POST `/api/v1/cashback/calculate`

Calculates cashback based on purchase parameters.

**Request body:**

```json
{
  "customer_type": "vip",      // "regular" or "vip"
  "purchase_amount": 600,      // in BRL (R$)
  "discount_percent": 15       // 0-100
}
```

**Response:**

```json
{
  "original_amount": 600.00,
  "discount_percent": 15,
  "discount_amount": 90.00,
  "final_amount": 510.00,
  "base_cashback_percent": 5,
  "base_cashback_amount": 25.50,
  "multiplier_applied": 1,     // 1 or 2
  "vip_bonus_applied": false,   // true/false
  "vip_bonus_amount": 0,
  "total_cashback": 25.50
}
```

### GET `/api/v1/cashback/history`

Returns cashback calculation history for the requesting IP address.

**Response:**

```json
{
  "history": [
    {
      "id": "abc-123",
      "customer_type": "vip",
      "purchase_amount": 600,
      "discount_percent": 15,
      "final_amount": 510.00,
      "total_cashback": 25.50,
      "created_at": "2026-04-15T10:30:00"
    }
  ]
}
```

## Testing

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Expected output:

```
... (3 tests in my case)
3 passed in 0.15s
```

## Production Deployment

- **Frontend:** https://cashback-app-nine.vercel.app/
- **Backend API:** Configured via environment variables (CORS allows frontend domain)

The production frontend consumes the production API directly.

### Frontend Note

- The frontend uses the URL configured in `frontend/config.js` to call the API
- During local development, it points to the local backend (`http://localhost:8000`) when no explicit configuration exists
- In production, it uses the deployed API URL

## Database

The application automatically creates tables on startup for local development convenience.

**Development:** Auto-create tables enabled (simpler setup)
**Production:** Prefer Alembic migrations (recommended)

### Schema

```sql
-- Cashback history table
CREATE TABLE IF NOT EXISTS cashback_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ip_address VARCHAR(45) NOT NULL,
    customer_type VARCHAR(10) NOT NULL,
    purchase_amount DECIMAL(10,2) NOT NULL,
    discount_percent DECIMAL(5,2) NOT NULL,
    final_amount DECIMAL(10,2) NOT NULL,
    total_cashback DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster IP lookups
CREATE INDEX IF NOT EXISTS idx_ip_address ON cashback_history(ip_address);
```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cashback_db

# CORS (comma-separated origins)
ALLOWED_ORIGINS=http://localhost:5500,https://cashback-app-nine.vercel.app

# Environment
ENVIRONMENT=development  # or "production"
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── database.py      # DB connection & setup
│   │   ├── models.py        # Pydantic models
│   │   ├── routes.py        # API endpoints
│   │   └── cashback.py      # Business logic
│   ├── tests/
│   │   └── test_cashback.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── config.js            # API URL configuration
├── docker-compose.yml
└── README.md
```

## Troubleshooting

### Database connection fails

```bash
# Check if PostgreSQL is running
docker ps

# View logs
docker compose logs postgres

# Restart database
docker compose restart postgres
```

### CORS errors in production

Make sure `ALLOWED_ORIGINS` in `.env` includes your frontend URL exactly (no trailing slash):

```
ALLOWED_ORIGINS=https://cashback-app-nine.vercel.app
```

### Port already in use

```bash
# Change port in .env or kill the process
lsof -i :8000
kill -9 <PID>
```

## Future Improvements

- [ ] Add Alembic for production migrations
- [ ] Add JWT authentication for admin endpoints
- [ ] Add pagination to history endpoint
- [ ] Add unit tests for edge cases (negative values, extreme discounts)
- [ ] Add Dockerfile for backend deployment

## Author

**Luis Octávius** - [GitHub](https://github.com/luis-octavius)

## Live Demo

- **Frontend:** https://cashback-app-nine.vercel.app/
- **API Base URL (production):** Configured in frontend config



· SQL · Git · Concurrency
```
