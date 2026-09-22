# Environment and hosts

## Local

| Service | URL |
|---------|-----|
| Customer platform | http://localhost:3000 |
| CRM / DASH | http://localhost:3001 |
| API | http://localhost:8000 |
| Swagger | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI | http://127.0.0.1:8000/openapi.json |
| Health | http://127.0.0.1:8000/api/health |

## Production (from deploy docs)

| Piece | Value |
|-------|--------|
| GCP project | `amaravisa-hub` |
| Cloud Run | `passage-api` in `asia-south1` |
| Image | `asia-south1-docker.pkg.dev/amaravisa-hub/passage/passage-api:latest` |
| Public site | `https://www.amaravisa.com` |
| CRM | `https://crm.amaravisa.com` |
| Extra customer origin | `https://dash.amaravisa.com` |
| Frontends | Two Vercel projects from `visaconsultantcrm-frontend` |

Production interactive docs: `https://<passage-api-host>/docs` (same FastAPI app). Confirm the live host with `GET /api/health`.

## Frontend env (consumers)

### CRM (`crm/.env` / Vercel)

| Variable | Purpose |
|----------|---------|
| `REACT_APP_BACKEND_URL` | API origin **without** `/api` |

### Customer (`customer/.env.local` / Vercel)

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_BACKEND_URL` | API origin without `/api` |
| `NEXT_PUBLIC_CRM_URL` | Link to staff login (default `http://localhost:3001/login`) |
| `NEXT_PUBLIC_SITE_URL` | Canonical origin for SEO **and** Upload-from-Mobile QR base (must be phone-reachable; set LAN IP for local dual-device QA) |
| `NEXT_PUBLIC_APP_URL` | Optional QR alias; `SITE_URL` wins if both set |
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Google sign-in |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | |
| `NEXT_PUBLIC_ALLOW_MOCK_PAYMENT` | Show mock checkout when API `PAYMENT_MODE=mock` |
| `NEXT_PUBLIC_SUPPORT_EMAIL` / `PHONE` / `WHATSAPP` | Contact |
| `NEXT_PUBLIC_OFFICE_MAPS_URL` | Maps link |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | GA4 |

## API env that changes client behaviour

| Variable | Consumer impact |
|----------|-----------------|
| `CORS_ORIGINS` | Browser origin must be listed (local 3000+3001; prod Vercel + amaravisa hosts) |
| `PAYMENT_MODE` / `RAZORPAY_KEY_ID` | Checkout returns `mock` vs Razorpay.js `key_id` |
| `FIREBASE_PROJECT_ID` | Google login fails with 503 if unset |
| `RESEND_API_KEY` | OTP / reset emails |
| `BUCKET_PUBLIC_URL` | Product banner URLs |
| `AUTH_OTP_DEBUG` | Local only — never enable in production |

## API env that must stay server-side

`MONGO_URL`, `DB_NAME`, `JWT_SECRET`, `PII_MASTER_KEY`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`, `FIREBASE_CREDENTIALS_JSON`, bucket/S3 credentials, `OCR_*`, `SEED_ON_STARTUP`, `RUN_MIGRATIONS_ON_STARTUP`.

## CORS example (production template)

```
https://www.amaravisa.com,https://amaravisa.com,https://dash.amaravisa.com,https://crm.amaravisa.com,<customer-vercel>,<crm-vercel>
```

Local default: `http://localhost:3000,http://localhost:3001`.

## Seed staff (local / demo only)

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@visaconsult.demo` | `Admin@123` |
| Consultant | `priya.consultant@visaconsult.demo` | `Consult@123` |

Do not use these as production credentials.
