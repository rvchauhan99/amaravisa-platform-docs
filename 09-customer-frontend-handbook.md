# Customer frontend handbook

**Audience:** engineers rebuilding or upgrading the **public customer site** only.

There is **one** Visa Consultancy API. The staff CRM is a separate client. For this handoff, treat CRM as **out of scope**.

## Out of scope (do not start here)

| Doc / area | Why |
|------------|-----|
| [05-api-catalog-crm.md](05-api-catalog-crm.md) | Staff pipeline / reports |
| [06-api-catalog-admin.md](06-api-catalog-admin.md) | Product Builder, Role Master, User Master |
| CRM Product Builder / Plans & pricing releases | Admin-only UX |
| Role Master `menu_keys` in [03](03-authentication-and-rbac.md) | Staff RBAC |

You only need the **Customer auth** and **Mobile upload session** sections of [03-authentication-and-rbac.md](03-authentication-and-rbac.md).

## Contract rule

- **UI may be redesigned** (layout, components, branding).
- **API contracts and business rules must match** this pack: paths, auth, payloads, step rules, payment modes, variant selection.

## Local stack

| Service | Typical URL |
|---------|-------------|
| API | `http://localhost:8000` |
| Customer app | `http://localhost:3000` (use another free port if busy) |
| Swagger | `http://localhost:8000/docs` |

Set `NEXT_PUBLIC_BACKEND_URL` to the API **origin without** `/api` (e.g. `http://localhost:8000`). Clients append `/api` themselves.

Full env matrix: [08-environment-and-hosts.md](08-environment-and-hosts.md) (see the customer FE checklist at the top).

## Route map

| Route | Purpose |
|-------|---------|
| `/` | Destination / visa catalog |
| `/visa/[productId]` | Product detail + plan picker (multi-SKU) |
| `/apply/[productId]` | Apply wizard |
| `/auth` | Register, OTP, login, Google, forgot password |
| `/account` | Profile, drafts, cases, travelers, vault, notifications |
| `/status/[caseId]` | Case status, payment proof, siblings |
| `/transparency/price-change-log` | Public fee change history |
| `/coming-soon` | Marketing stub (no API) |

Screen → API overview: [02-architecture-and-integration.md](02-architecture-and-integration.md) (customer table). Deep contracts: [10](10-customer-apply-and-checkout.md), [11](11-customer-variants-and-pricing-ui.md).

## Session and HTTP client

| Item | Value |
|------|--------|
| Token storage | `sessionStorage` key `vc_customer_token` (tab-scoped) |
| User storage | `sessionStorage` key `vc_customer_user` |
| Header | `Authorization: Bearer <access_token>` |
| On **401** | Clear customer session keys and send user to `/auth` |

Do not put `JWT_SECRET`, Mongo, Cashfree secrets, or bank account secrets in the frontend.

## Auth (customer)

| Flow | Endpoints |
|------|-----------|
| Email register | `POST /api/auth/customer/register` → OTP → `verify-otp` |
| Login | `POST /api/auth/customer/login` |
| Google | Firebase ID token → `POST /api/auth/customer/google` |
| Forgot password | `forgot-password` → `forgot-password/reset` |

Details: [03-authentication-and-rbac.md](03-authentication-and-rbac.md) (Customer auth). Mobile QR uploads may use `session_id` instead of JWT — see [10](10-customer-apply-and-checkout.md).

## Reading order

1. This handbook  
2. [11-customer-variants-and-pricing-ui.md](11-customer-variants-and-pricing-ui.md)  
3. [10-customer-apply-and-checkout.md](10-customer-apply-and-checkout.md)  
4. [12-customer-response-shapes.md](12-customer-response-shapes.md)  
5. [04-api-catalog-customer.md](04-api-catalog-customer.md)  
6. [07-payloads-and-models.md](07-payloads-and-models.md) (request models)  
7. [openapi/api-examples.json](openapi/api-examples.json) (dummy bodies)  
8. [08-environment-and-hosts.md](08-environment-and-hosts.md)  

Live API: production Swagger `https://api.amaravisa.com/docs` · local `http://localhost:8000/docs`.

## Current reference implementation

Legacy/reference Next.js app lives in `visaconsultantcrm-frontend/customer/`. Use it for behaviour checks, not as a required visual design system.
