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

## Production

| Piece | Value |
|-------|--------|
| API | `https://api.amaravisa.com` (VPS) |
| API resources | 4.5 GB RAM and 1.75 CPU of the 6 GB / 2 vCPU VPS. Test containers stay capped lower. |
| Health | `https://api.amaravisa.com/api/health` |
| Swagger | `https://api.amaravisa.com/docs` |
| Public site | `https://www.amaravisa.com` |
| CRM | `https://crm.amaravisa.com` |
| Extra customer origin | `https://dash.amaravisa.com` |
| Frontends | Two Vercel projects from `visaconsultantcrm-frontend` |
| Cloud Run (rollback, not deleted yet) | `https://passage-api-kl2h4tfmqa-el.a.run.app` |

Vercel env (no `/api` suffix):

| Project | Variable | Value |
|---------|----------|--------|
| Customer | `NEXT_PUBLIC_BACKEND_URL` | `https://api.amaravisa.com` |
| CRM | `REACT_APP_BACKEND_URL` | `https://api.amaravisa.com` |

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
| `NEXT_PUBLIC_ALLOW_MOCK_PAYMENT` | Unused while bank-transfer checkout is on (gateway hardcoded off). |
| `NEXT_PUBLIC_SUPPORT_EMAIL` / `PHONE` / `WHATSAPP` | Contact |
| `NEXT_PUBLIC_OFFICE_MAPS_URL` | Maps link |
| `NEXT_PUBLIC_GA_MEASUREMENT_ID` | GA4 |

## API env that changes client behaviour

| Variable | Consumer impact |
|----------|-----------------|
| `CORS_ORIGINS` | Browser origin must be listed (local 3000+3001; prod Vercel + amaravisa hosts) |
| `CASHFREE_CLIENT_ID` / `CASHFREE_CLIENT_SECRET` | When both are set, `/apply` checkout uses Cashfree. `CASHFREE_APP_ID` and `CASHFREE_SECRET_KEY` are accepted aliases. When either value is empty, checkout stays `bank_transfer`. Orders use Cashfree API version `2025-01-01`. |
| `CASHFREE_ENV` | `sandbox` (default) or `production`. Returned to the customer app as `cashfree_env` so the JS checkout uses the same mode. |
| `PAYMENT_MODE` / `RAZORPAY_KEY_ID` | Ignored while `GATEWAY_ENABLED` is False and Cashfree is unset. |
| `PAYMENT_BANK_NAME` / `PAYMENT_ACCOUNT_NAME` / `PAYMENT_ACCOUNT_NUMBER` / `PAYMENT_IFSC` / `PAYMENT_BRANCH_NAME` / `PAYMENT_UPI_ID` | Customer `/apply` Payment (`GET /api/payment/bank-details`). Empty values omit that row; empty UPI hides QR. |
| `PAYMENT_CUST_ID` | HDFC customer id — staff/ops only; never on the customer bank-details payload. |
| `FIREBASE_PROJECT_ID` | Google login fails with 503 if unset |
| `RESEND_API_KEY` | OTP / reset emails |
| `BUCKET_PUBLIC_URL` | Product banner URLs |
| `AUTH_OTP_DEBUG` | Local only — never enable in production |

## API env that must stay server-side

`MONGO_URL`, `DB_NAME`, `JWT_SECRET`, `PII_MASTER_KEY`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`, `CASHFREE_CLIENT_ID`, `CASHFREE_CLIENT_SECRET`, `FIREBASE_CREDENTIALS_JSON`, bucket/S3 credentials, `OCR_*`, `SEED_ON_STARTUP`, `RUN_MIGRATIONS_ON_STARTUP`.

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
