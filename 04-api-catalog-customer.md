# API catalog — customer platform and public

These endpoints power the **customer site** (Next.js) and public catalog. Base URL is the API origin plus `/api`.

Interactive docs: [Swagger UI](http://127.0.0.1:8000/docs) · [ReDoc](http://127.0.0.1:8000/redoc) · snapshot in [`openapi/openapi.json`](openapi/openapi.json).

Auth column is from the live route guards (OpenAPI does not always mark security). Request body names match Pydantic models — field lists are in [07-payloads-and-models.md](07-payloads-and-models.md).


**42 operations** in this catalog.

## other

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/` | public |  |  | Root |
| GET | `/api/health` | public |  |  | Health |

## auth

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| POST | `/api/auth/customer/forgot-password` | public | CustomerForgotPasswordIn |  | Customer Forgot Password |
| POST | `/api/auth/customer/forgot-password/reset` | public | CustomerForgotPasswordResetIn |  | Customer Forgot Password Reset |
| POST | `/api/auth/customer/google` | public | CustomerGoogleIn |  | Customer Google |
| POST | `/api/auth/customer/login` | public | LoginIn |  | Customer Login |
| POST | `/api/auth/customer/register` | public | CustomerRegisterIn |  | Customer Register |
| POST | `/api/auth/customer/register/resend-otp` | public | CustomerResendOtpIn |  | Customer Register Resend Otp |
| POST | `/api/auth/customer/register/verify-otp` | public | CustomerVerifyOtpIn |  | Customer Register Verify Otp |

## cases

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| POST | `/api/cases` | customer JWT | CaseDraftIn |  | Save Draft |
| POST | `/api/cases/checkout` | customer JWT | PaymentConfirmIn |  | Checkout Confirm |
| POST | `/api/cases/checkout/create-order` | customer JWT | MockCheckoutIn |  | Create Payment Order |
| GET | `/api/cases/drafts` | customer JWT |  |  | List Drafts |
| GET | `/api/cases/drafts/{draft_id}` | customer JWT |  |  | Get Draft |
| PATCH | `/api/cases/drafts/{draft_id}` | customer JWT | CaseDraftPatchIn |  | Update Draft |
| POST | `/api/cases/drafts/{draft_id}/travelers` | customer JWT | object |  | Add Draft Traveler |
| DELETE | `/api/cases/drafts/{draft_id}/travelers/{traveler_id}` | customer JWT |  |  | Remove Draft Traveler |
| GET | `/api/cases/groups/{group_id}` | customer JWT |  |  | Get My Case Group |
| GET | `/api/cases/my` | customer JWT |  |  | My Cases |
| GET | `/api/cases/notifications/portal` | customer JWT |  |  | Portal Notifications |
| POST | `/api/cases/webhooks/razorpay` | webhook HMAC |  |  | Razorpay Webhook |
| POST | `/api/cases/{case_id}/documents/{doc_id}/resubmit` | customer JWT | DocumentResubmitIn |  | Resubmit Document |
| GET | `/api/cases/{case_id}/receipt` | customer JWT |  |  | Case Receipt |
| GET | `/api/cases/{case_id}/status` | customer JWT |  |  | Case Status |

## customer_master

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/customers/me` | customer JWT |  |  | Me |
| PATCH | `/api/customers/me` | customer JWT | CustomerProfileIn |  | Update Me |
| GET | `/api/customers/me/notifications` | customer JWT |  |  | My Portal Notifications |
| POST | `/api/customers/me/notifications/mark-all-read` | customer JWT |  |  | Mark All Notifications Read |

## document_vault

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/customers/me/document-vault` | customer JWT |  |  | List Vault |
| GET | `/api/customers/me/document-vault/by-key/{doc_key}` | customer JWT |  |  | List Vault By Key |
| DELETE | `/api/customers/me/document-vault/{vault_id}` | customer JWT |  |  | Delete Vault Item |

## traveler_profiles

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/customers/me/traveler-profiles` | customer JWT |  |  | List Profiles |
| POST | `/api/customers/me/traveler-profiles` | customer JWT | TravelerProfileIn |  | Create Profile |
| DELETE | `/api/customers/me/traveler-profiles/{profile_id}` | customer JWT |  |  | Delete Profile |
| GET | `/api/customers/me/traveler-profiles/{profile_id}` | customer JWT |  |  | Get Profile |
| PATCH | `/api/customers/me/traveler-profiles/{profile_id}` | customer JWT | TravelerProfileIn |  | Update Profile |

## documents

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/documents/download` | signed `token` query |  | token | Download |
| POST | `/api/documents/scan-passport` | customer JWT | multipart/form-data (`file`) |  | Scan Passport |
| POST | `/api/documents/upload` | customer JWT | multipart/form-data (`file`) | doc_key | Upload Document |

## visa_products

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/visa-products` | public |  | country, visa_type, visa_format, documents_profile, q, complexity, travel_date, limit, offset, id | List Public Products |
| GET | `/api/visa-products/countries` | public |  | q, limit, offset, id | List Countries (full ISO-3 world list + custom `SCH` Schengen; `id` = country code) |
| GET | `/api/visa-products/{product_id}` | public |  |  | Get Product Detail |
