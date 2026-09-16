# Architecture and integration

## One API, two clients

```
Customer site (Next.js :3000)          Staff CRM (CRA :3001)
amaravisa.com / dash.amaravisa.com     crm.amaravisa.com
        |                                      |
        |  NEXT_PUBLIC_BACKEND_URL             |  REACT_APP_BACKEND_URL
        |  + /api                              |  + /api
        +------------------+-------------------+
                           |
                  Visa Consultancy API
                  FastAPI  /api/*
                  Cloud Run passage-api
                           |
                       MongoDB
```

Both axios clients send `Authorization: Bearer <token>` when a session exists. A **401** clears the local session.

## Surfaces

| Name in the email | Product | Typical host | Client env |
|-------------------|---------|--------------|------------|
| Platform | Customer Next.js app | `https://www.amaravisa.com`, also `dash.amaravisa.com` in CORS | `NEXT_PUBLIC_BACKEND_URL` |
| DASH / CRM | Staff CRA app | `https://crm.amaravisa.com` | `REACT_APP_BACKEND_URL` |
| Connecting APIs | FastAPI | Cloud Run `passage-api` | origin only, no `/api` suffix |

`dash.amaravisa.com` is **not** a second API. It is an allowed browser origin for the customer app.

## Customer platform — page to API

| Page | Typical APIs |
|------|----------------|
| `/` home catalog | `GET /api/visa-products`, `GET /api/visa-products/countries` (SSR/ISR + client) |
| `/visa/[productId]` | `GET /api/visa-products/{product_id}` |
| `/auth` | `POST /api/auth/customer/register`, `verify-otp`, `resend-otp`, `login`, `google`, `forgot-password` |
| `/apply/[productId]` | Dynamic steps: Party (1–6 travelers) → Details (if fields, per traveler) → Documents (if product docs, per traveler) → Review → Payment (fees × N). Passport scan + passport fields only when `passport_scan` is on the product. APIs: `POST /api/cases` (`travelers[]`), `PATCH /api/cases/drafts/{id}`, traveler add/remove, `POST /api/documents/upload`, `POST /api/documents/scan-passport`, checkout → N linked cases + `case_group_id` |
| `/status/[caseId]` | `GET /api/cases/{case_id}/status` (includes `sibling_cases` / `case_group` when grouped); UI shows “Part of family booking (i of N)” + sibling links; document resubmit |
| `/account` | `GET/PATCH /api/customers/me`, traveler-profiles, document-vault; application cards show Family · N travelers when grouped |

## CRM / DASH — page to API

| CRM route | Typical APIs | Menu key |
|-----------|--------------|----------|
| `/` Dashboard | `GET /api/crm/reports/dashboard` | `dashboard` |
| `/reports` | `GET /api/crm/reports/*` | `case_reports` |
| `/reports/payments` | `GET /api/crm/payments`, `/api/crm/reports/payments` | `payment_reports` |
| `/leads/analysis` | `GET /api/crm/reports/leads` | `lead_analytics` |
| `/pipeline`, `/cases/:id` | `GET /api/crm/cases` (group enrichment: `case_group_id`, `traveler_count`, `group_members`, `group_has_lagging_sibling`). Board collapses multi-traveler siblings into one expandable group card under the primary member’s stage; case detail shows family booking banner + sibling links. `GET /api/crm/case-groups/{id}`, case mutations | `pipeline` |
| `/cases/closed` | `GET /api/crm/cases` (closed filters) | `closed_cases` |
| `/offline-case` | `POST /api/crm/cases` (optional `travelers[]` 1–6 → N linked cases; redirect to primary `case_id`) | `offline_case` |
| `/tasks` | `/api/crm/tasks*` | `tasks` |
| `/leads`, `/leads/new` | `/api/crm/leads*` | `leads` (UI) |
| `/follow-ups` | `/api/crm/lead-follow-ups*` | `follow_ups` (UI) |
| `/clients`, `/clients/:id` | `/api/crm/clients*` (case history/recent work include `case_group_id` for family badge) | `clients` |
| `/service-orders` | `/api/crm/service-orders*` | `service_orders` |
| `/finance` | invoices / quotations / payments | `finance` (UI) |
| `/inbox` | `/api/crm/communications*` | `inbox` (UI) |
| `/passport-expiry` | `/api/crm/passport-expiry*` | `passport_expiry` |
| `/birthdays` | `GET /api/crm/birthdays` | `birthdays` |
| `/products` | `/api/admin/visa-products*` | `visa_products` |
| `/passport-products` | `/api/admin/passport-products*` | `passport_products` |
| `/document-master` | `/api/admin/document-master*` | `document_master` |
| `/field-master` | `/api/admin/field-master*` | `field_master` |
| `/consultants` User Master | `/api/admin/consultants*`, `GET /api/admin/roles` | `user_master` |
| `/roles` Role Master | `/api/admin/roles*` | `role_master` |
| `/case-number-settings` | `/api/admin/settings/case-number-format` | `case_numbers` |
| `/profile` | `/api/staff/me*`, staff 2FA | staff only (no menu) |
| `/login` | `POST /api/auth/staff/login`, `verify-2fa` | public |

Always-on staff utilities (no menu): `GET /api/crm/notifications*`, `GET /api/crm/search`, `GET /api/documents/download` (signed URL).

## Integration rules for a new client

1. Call `{API_ORIGIN}/api/...` over HTTPS.
2. Send `Authorization: Bearer` for protected routes.
3. List the browser origin in API `CORS_ORIGINS`.
4. Do not send `JWT_SECRET`, Mongo, or Razorpay secret from a frontend.
5. Customer sessions are tab-scoped (`sessionStorage`). CRM sessions persist in `localStorage`.

Storage keys:

| App | Token key | User key |
|-----|-----------|----------|
| CRM | `vc_staff_token` (localStorage) | `vc_staff_user` |
| Customer | `vc_customer_token` (sessionStorage) | `vc_customer_user` |
