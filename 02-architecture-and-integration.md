# Architecture and integration

## One API, two clients

```
Customer site (Next.js)                Staff CRM (CRA)
www.amaravisa.com / dash.amaravisa.com crm.amaravisa.com
        |                                      |
        |  NEXT_PUBLIC_BACKEND_URL             |  REACT_APP_BACKEND_URL
        |  + /api                              |  + /api
        +------------------+-------------------+
                           |
                  Visa Consultancy API
                  FastAPI  /api/*
                  api.amaravisa.com (VPS)
                  Cloud Run = rollback only
                           |
                       MongoDB
```

Customer rebuild handbook: [09-customer-frontend-handbook.md](09-customer-frontend-handbook.md).

Both axios clients send `Authorization: Bearer <token>` when a session exists. A **401** clears the local session.

## Surfaces

| Name in the email | Product | Typical host | Client env |
|-------------------|---------|--------------|------------|
| Platform | Customer Next.js app | `https://www.amaravisa.com`, also `dash.amaravisa.com` in CORS | `NEXT_PUBLIC_BACKEND_URL` |
| DASH / CRM | Staff CRA app | `https://crm.amaravisa.com` | `REACT_APP_BACKEND_URL` |
| Connecting APIs | FastAPI | `https://api.amaravisa.com` (VPS; Cloud Run rollback) | origin only, no `/api` suffix |

`dash.amaravisa.com` is **not** a second API. It is an allowed browser origin for the customer app.

## Customer platform — page to API

| Page | Typical APIs |
|------|----------------|
| `/` home catalog | `GET /api/visa-products`, `GET /api/visa-products/countries` (SSR/ISR + client). **Guaranteed Visa On** = calendar `today + processing_time_days` (no weekend/holiday skip). See [11](11-customer-variants-and-pricing-ui.md). |
| `/visa/[productId]` | `GET /api/visa-products/{product_id}` (`variant_id?`). Multi-SKU picker when `variant_count > 1` — grouping + chips in [11](11-customer-variants-and-pricing-ui.md). Fee card → fee-change history for `country_code`. Shapes: [12](12-customer-response-shapes.md). |
| `/transparency/price-change-log?search=` | Public fee change history (columns: Date, **Plan**, Fee Type, From, To, Difference, Reason — no Product column in UI; Plan = `variant_label` or `—`). `GET /api/visa-products/fee-change-log`. |
| `/auth` | `POST /api/auth/customer/register`, `verify-otp`, `resend-otp`, `login`, `google`, `forgot-password` |
| `/apply/[productId]` | Full step + payment contract: [10-customer-apply-and-checkout.md](10-customer-apply-and-checkout.md). Party → Details (if fields) → Documents (skip if none) → Review → Payment. Wait for `create-order` before Payment UI. Cashfree or bank_transfer. Mobile QR upload: single traveler only. |
| `/status/[caseId]` | `GET /api/cases/{case_id}/status` (siblings, payment proof). See [10](10-customer-apply-and-checkout.md) status loop. |
| `/account` | `GET/PATCH /api/customers/me`, traveler-profiles, document-vault; application cards show Family · N travelers when grouped |
| `/coming-soon` | Marketing stub — no API |

See also: [Release note — Manual bank payment and CRM confirmation](releases/2026-09-28-manual-bank-payment.md) (28 Sep 2026).

## CRM / DASH — page to API

**Staff only.** Customer-site rebuilds can ignore this table.

| CRM route | Typical APIs | Menu key |
|-----------|--------------|----------|
| `/` Dashboard | `GET /api/crm/reports/dashboard` | `dashboard` |
| `/reports` | `GET /api/crm/reports/*` | `case_reports` |
| `/reports/payments` | `GET /api/crm/payments`, `/api/crm/reports/payments` | `payment_reports` |
| `/leads/analysis` | `GET /api/crm/reports/leads` | `lead_analytics` |
| `/pipeline`, `/cases/:id` | `GET /api/crm/cases` (group enrichment: `case_group_id`, `traveler_count`, `group_members`, `group_has_lagging_sibling`). Board collapses multi-traveler siblings into one expandable group card under the primary member’s stage; case detail shows family booking banner + sibling links. Payment tab: proof preview, UTR confirm / reject (`POST /api/crm/cases/{id}/payment/confirm`, `.../reject-proof`, `pipeline` menu). `GET /api/crm/case-groups/{id}`, case mutations | `pipeline` |
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
| `/products` | `/api/admin/visa-products*` — Product Builder tabs: Basic, Documents, Fields, **Plans & pricing** (`pb-tab-variants`). **No Pricing tab** — fees only on Plans & pricing via `POST .../variants/{id}/fees` (reason **min 10 chars**, live count). `POST .../fees` (omit `variant_id`) remains API/compat for default plan. Publish via `PATCH .../publish` / `GET .../can-publish` (**zero required docs allowed**; every active plan must have fees + processing). Multi-SKU: Basic hides validity/processing; edit plans on Plans & pricing. Customer `/visa/{id}` shows a picker only when `variant_count > 1`. Customer `/apply` omits Documents when the product has no docs. | `visa_products`, `visa_product_variants` |
| `/passport-products` | `/api/admin/passport-products*` — same publish rules as visa (0 required docs allowed). | `passport_products` |
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
