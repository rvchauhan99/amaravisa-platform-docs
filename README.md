# AmaraVisa platform documentation

This pack answers the team request for:

1. **Technology stack** — current front-end and back-end frameworks
2. **API documentation and integration** — every API that connects the customer platform and the CRM / DASH, with endpoints, payloads, and documentation links

It was produced from a **full code review** of the two Git repositories (not from marketing copy):

| Source repo | Role |
|-------------|------|
| `visaconsultantcrm-frontend` | Customer site + staff CRM |
| `visaconsultantcrm-backend` | Shared Visa Consultancy API |

This folder is a **standalone documentation repository**. It is not part of the CRM or backend remotes.

---

## Direct answers

### Technology stack

| Surface | What it is | Frameworks |
|---------|------------|------------|
| **Customer platform** (public site) | Next.js app in `visaconsultantcrm-frontend/customer/` | Next.js 15 App Router, React 19, Tailwind CSS 4, Axios, Firebase (Google sign-in) |
| **CRM / DASH** (staff ops) | CRA app in `visaconsultantcrm-frontend/crm/` | Create React App 5 + CRACO, React 19, React Router 7, Tailwind CSS 3, shadcn/Radix, Axios |
| **API** | FastAPI service in `visaconsultantcrm-backend/` | Python 3.11, FastAPI 0.110, MongoDB (Motor), JWT, Razorpay, Resend, Cloudflare R2/S3 |

Full library and hosting detail: [01-technology-stack.md](01-technology-stack.md).

### How DASH / CRM connects to the platform

There is **one backend**. There is no separate DASH API.

- **Customer platform** calls public catalog + customer-auth + `/api/cases` + `/api/customers/me`.
- **CRM / DASH** calls staff-auth + `/api/crm/*` + `/api/admin/*` + `/api/staff/me`.
- `dash.amaravisa.com` is a CORS origin for the **customer** site. Staff CRM is `crm.amaravisa.com`.

See [02-architecture-and-integration.md](02-architecture-and-integration.md).

### API documentation links

| Document | URL / file |
|----------|------------|
| Swagger UI (live local) | http://127.0.0.1:8000/docs |
| ReDoc (live local) | http://127.0.0.1:8000/redoc |
| OpenAPI JSON (live local) | http://127.0.0.1:8000/openapi.json |
| OpenAPI snapshot in this pack | [openapi/openapi.json](openapi/openapi.json) |
| **Dummy request + response for every API** | [openapi/api-examples.json](openapi/api-examples.json) |
| Customer + public catalog | [04-api-catalog-customer.md](04-api-catalog-customer.md) |
| CRM / DASH catalog | [05-api-catalog-crm.md](05-api-catalog-crm.md) |
| Admin / Role Master / User Master | [06-api-catalog-admin.md](06-api-catalog-admin.md) |
| Request/response field lists | [07-payloads-and-models.md](07-payloads-and-models.md) |
| Auth, JWT, Role Master menus | [03-authentication-and-rbac.md](03-authentication-and-rbac.md) |
| Hosts, CORS, env vars | [08-environment-and-hosts.md](08-environment-and-hosts.md) |
| Passport OCR (existing) | summarised from backend `docs/passport-ocr/api.md` |

Production Swagger is the same FastAPI app on Cloud Run: `https://<passage-api-host>/docs`.

---

## How to read this pack

1. Start here and [01-technology-stack.md](01-technology-stack.md).
2. Use [02-architecture-and-integration.md](02-architecture-and-integration.md) for screen-to-API mapping.
3. Use catalogs 04–06 for method, path, auth, body, and query parameters.
4. Use [07-payloads-and-models.md](07-payloads-and-models.md) for field-level payloads.
5. Copy dummy request/response bodies from [openapi/api-examples.json](openapi/api-examples.json) (177 operations).
6. Import [openapi/openapi.json](openapi/openapi.json) into Postman / Insomnia if you need a machine-readable spec.

Base URL for all HTTP paths in the catalogs is:

```
{API_ORIGIN}/api/...
```

Local default: `http://127.0.0.1:8000`. Clients set `REACT_APP_BACKEND_URL` / `NEXT_PUBLIC_BACKEND_URL` to the origin **without** `/api`; they append `/api` themselves.

---

## Regenerating the catalogs

With the API running on port 8000:

```bash
curl -sS -o openapi/openapi.json http://127.0.0.1:8000/openapi.json
python3 scripts/generate_catalogs.py
python3 scripts/generate_examples.py
```
