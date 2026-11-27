# amaravisa platform documentation

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

## Customer site rebuild (frontend hire)

If you are rebuilding or upgrading **only the public customer site**, start here and **ignore CRM/admin docs**.

| Step | Doc |
|------|-----|
| 1. Handbook (scope, routes, session) | [09-customer-frontend-handbook.md](09-customer-frontend-handbook.md) |
| 2. Plans / multi-SKU UI | [11-customer-variants-and-pricing-ui.md](11-customer-variants-and-pricing-ui.md) |
| 3. Apply + checkout | [10-customer-apply-and-checkout.md](10-customer-apply-and-checkout.md) |
| 4. Response shapes to bind | [12-customer-response-shapes.md](12-customer-response-shapes.md) |
| 5. Endpoint catalog | [04-api-catalog-customer.md](04-api-catalog-customer.md) |
| 6. Request models | [07-payloads-and-models.md](07-payloads-and-models.md) |
| 7. Dummy JSON | [openapi/api-examples.json](openapi/api-examples.json) |
| 8. Env / hosts | [08-environment-and-hosts.md](08-environment-and-hosts.md) |

**Out of scope for the customer hire:** [05-api-catalog-crm.md](05-api-catalog-crm.md), [06-api-catalog-admin.md](06-api-catalog-admin.md), Role Master menus, CRM Product Builder / Plans & pricing admin UI. Staff auth beyond what the customer app links to (`NEXT_PUBLIC_CRM_URL`) is not required.

**Contract:** UI redesign is allowed; API paths, payloads, and business rules in this pack are required.

---

## Direct answers

### Technology stack

| Surface | What it is | Frameworks |
|---------|------------|------------|
| **Customer platform** (public site) | Next.js app in `visaconsultantcrm-frontend/customer/` | Next.js 15 App Router, React 19, Tailwind CSS 4, Axios, Firebase (Google sign-in) |
| **CRM / DASH** (staff ops) | CRA app in `visaconsultantcrm-frontend/crm/` | Create React App 5 + CRACO, React 19, React Router 7, Tailwind CSS 3, shadcn/Radix, Axios |
| **API** | FastAPI service in `visaconsultantcrm-backend/` | Python 3.11, FastAPI 0.110, MongoDB (Motor), JWT, Cashfree or bank transfer, Resend, Cloudflare R2/S3 |

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
| Customer FE handbook | [09-customer-frontend-handbook.md](09-customer-frontend-handbook.md) |
| Customer apply + checkout | [10-customer-apply-and-checkout.md](10-customer-apply-and-checkout.md) |
| Customer variants / pricing UI | [11-customer-variants-and-pricing-ui.md](11-customer-variants-and-pricing-ui.md) |
| Customer response shapes | [12-customer-response-shapes.md](12-customer-response-shapes.md) |
| CRM / DASH catalog (staff) | [05-api-catalog-crm.md](05-api-catalog-crm.md) |
| Admin / Role Master / User Master (staff) | [06-api-catalog-admin.md](06-api-catalog-admin.md) |
| Request/response field lists | [07-payloads-and-models.md](07-payloads-and-models.md) |
| Auth, JWT, Role Master menus | [03-authentication-and-rbac.md](03-authentication-and-rbac.md) |
| Hosts, CORS, env vars | [08-environment-and-hosts.md](08-environment-and-hosts.md) |
| Passport OCR (existing) | summarised from backend `docs/passport-ocr/api.md` |
| Releases | [2026-11-27 customer FE docs pack](releases/2026-11-27-customer-frontend-docs-pack.md), [2026-11-27 plans & pricing admin](releases/2026-11-27-plans-pricing-admin.md), [2026-11-27 visa product variants](releases/2026-11-27-visa-product-variants.md), [2026-11-23 fee reason min guideline](releases/2026-11-23-fee-reason-min-guideline.md), [2026-11-18 zero-doc publish](releases/2026-11-18-zero-doc-publish.md), [2026-11-08 fee change transparency](releases/2026-11-08-fee-change-transparency.md), [2026-11-05 brand lowercase](releases/2026-11-05-brand-lowercase.md), [2026-10-05 payment mode flash fix](releases/2026-10-05-payment-mode-flash-fix.md), [2026-10-05 VPS CI deploy](releases/2026-10-05-vps-ci-deploy.md), [2026-10-05 apply continue hooks fix](releases/2026-10-05-apply-continue-hooks-fix.md), [2026-10-05 Cashfree checkout](releases/2026-10-05-cashfree-checkout.md), [2026-09-28 manual bank payment](releases/2026-09-28-manual-bank-payment.md) |

Production Swagger: `https://api.amaravisa.com/docs`.

---

## How to read this pack

**Customer site only:** follow [Customer site rebuild](#customer-site-rebuild-frontend-hire) above.

**Full platform / staff:**

1. Start here and [01-technology-stack.md](01-technology-stack.md).
2. Use [02-architecture-and-integration.md](02-architecture-and-integration.md) for screen-to-API mapping.
3. Use catalogs 04–06 for method, path, auth, body, and query parameters.
4. Use [07-payloads-and-models.md](07-payloads-and-models.md) for field-level payloads.
5. Copy dummy request/response bodies from [openapi/api-examples.json](openapi/api-examples.json).
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

`generate_catalogs.py` rewrites the body of `04`/`05`/`06` from OpenAPI. After regenerating, restore the customer FE intro links and the `WS /api/documents/ws/{session_id}` row in [04-api-catalog-customer.md](04-api-catalog-customer.md) (OpenAPI does not list WebSockets). Response overrides for product detail / fee-log / status live in `scripts/generate_examples.py` (`RESPONSE_OVERRIDES`).
