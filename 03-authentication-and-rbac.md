# Authentication and Role Master RBAC

## Token

| Item | Value |
|------|--------|
| Type | JWT, algorithm HS256 |
| Header | `Authorization: Bearer <access_token>` |
| Lifetime | 12 hours |
| Claims | `sub`, `typ` (`customer` or `staff`), `role`, `email`, `tenant_id`, `iat`, `exp` |

Staff login and `GET /api/staff/me` also return application fields on the **user object** (not inside the JWT): `role_name`, `menu_keys`, `unrestricted_scope`, `country_codes`, `two_factor_enabled`.

## Customer auth

| Step | Endpoint |
|------|----------|
| Register | `POST /api/auth/customer/register` → `{ pending_token, email }` |
| Verify email OTP | `POST /api/auth/customer/register/verify-otp` → access token |
| Resend OTP | `POST /api/auth/customer/register/resend-otp` |
| Login | `POST /api/auth/customer/login` |
| Google | `POST /api/auth/customer/google` with Firebase `id_token` |
| Forgot password | `POST /api/auth/customer/forgot-password` then `/forgot-password/reset` |

OTP is 6 digits, 10 minutes, max 5 attempts. Pending token purpose: `customer_email_verify` (30 minutes).

## Staff auth

| Step | Endpoint |
|------|----------|
| Login | `POST /api/auth/staff/login` |
| If 2FA enabled | response `{ require_2fa, temp_token }` then `POST /api/auth/staff/verify-2fa` |
| Enable 2FA | `POST /api/auth/staff/2fa/generate` then `/enable` |
| Disable 2FA | `POST /api/auth/staff/2fa/disable` |
| Profile | `GET /api/staff/me` |

Temp token purpose: `staff_2fa_pending` (5 minutes). Inactive staff cannot authenticate.

## Guards

| Dependency | Meaning |
|------------|---------|
| Public | No JWT |
| Customer JWT | `typ == customer` |
| Staff JWT | `typ == staff`; live consultant must be `active` |
| Menu | Staff + at least one listed `menu_keys` on the live Role Master document |
| Unrestricted | System Admin role (`unrestricted_scope: true`) — all countries / all staff |
| Webhook | `X-Razorpay-Signature` |
| Download | Short-lived signed `token` query on `GET /api/documents/download` |

## Role Master

Users keep `consultants.role` as a **slug** (`admin`, `consultant`, or a custom slug). Menus live on the `roles` collection.

| Role | Menus | Data scope |
|------|-------|------------|
| `admin` (system) | All keys including `role_master` | Org-wide (`unrestricted_scope`) |
| `consultant` (system) | Insights + Cases + People + Operations + Client care | Assigned countries only |
| Custom | Checklist from Role Master | Assigned countries only (never org-wide) |

Country assignment stays on the **user** (`consultant_countries`). Admin has no country rows.

### Menu catalog

| Key | Unlocks (CRM) |
|-----|----------------|
| `dashboard` | `/` |
| `case_reports` | `/reports` |
| `payment_reports` | `/reports/payments` |
| `lead_analytics` | `/leads/analysis` |
| `pipeline` | `/pipeline`, `/cases/:id` |
| `closed_cases` | `/cases/closed` |
| `offline_case` | `/offline-case` |
| `tasks` | `/tasks` |
| `leads` | `/leads`, `/leads/new` |
| `clients` | `/clients` |
| `follow_ups` | `/follow-ups` |
| `service_orders` | `/service-orders` |
| `finance` | `/finance` |
| `inbox` | `/inbox` |
| `passport_expiry` | `/passport-expiry` |
| `birthdays` | `/birthdays` |
| `visa_products` | `/products` |
| `passport_products` | `/passport-products` |
| `document_master` | `/document-master` |
| `field_master` | `/field-master` |
| `user_master` | `/consultants` |
| `case_numbers` | `/case-number-settings` |
| `role_master` | `/roles` |

Always available without a menu: `/login`, `/profile`, notifications, signed file download.

### Lockouts

- System roles cannot be deleted or deactivated.
- Admin cannot drop `role_master` or `user_master`.
- Custom roles cannot set `unrestricted_scope`.
- A custom role cannot be deleted while users still have that slug.

## Rate limits (in-memory)

| Area | Limit |
|------|--------|
| `/api/auth` | 30 / 60s per IP+path |
| Visa catalog | 120 / 60s |
| Uploads | 40 / 60s |
| Passport OCR | 10 / 10 min |
