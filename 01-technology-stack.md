# Technology stack

Reviewed from `package.json`, `requirements.txt`, Docker, and deploy docs. Versions are those pinned in source at review time.

## Front end — customer platform

| Item | Detail |
|------|--------|
| Location | `visaconsultantcrm-frontend/customer/` |
| Package name | `visaconsultantcrm-customer` 0.2.0 |
| Framework | **Next.js 15.5.9** App Router |
| UI library | **React 19.1** |
| Language | JavaScript (no TypeScript) |
| Styling | **Tailwind CSS 4** (`@tailwindcss/postcss`) |
| HTTP | Axios |
| Server state | TanStack React Query 5 |
| Forms | react-hook-form, Zod |
| Auth extra | **Firebase 11** (Google ID token → API) |
| Icons / motion | Lucide, Framer Motion |
| Hosting | **Vercel** (Next.js project, root directory `customer`) |
| Local URL | http://localhost:3000 |

Shared design tokens live in `visaconsultantcrm-frontend/packages/ui` (`@passage/ui`).

A legacy CRA customer app exists at `customer-cra/` for reference only. It is not the production platform.

## Front end — CRM / DASH

| Item | Detail |
|------|--------|
| Location | `visaconsultantcrm-frontend/crm/` |
| Package name | `visaconsultantcrm-crm` 0.1.0 |
| Framework | **Create React App 5** + **CRACO 7** |
| UI library | **React 19.0** |
| Routing | **React Router DOM 7.15** |
| Language | JavaScript |
| Styling | **Tailwind CSS 3.4** |
| Component kit | **shadcn/ui** (New York) + **Radix UI** primitives |
| HTTP | Axios 1.18 |
| Charts / kanban | Recharts, @dnd-kit |
| Forms | react-hook-form, Zod |
| Toasts | Sonner |
| Hosting | **Vercel** (SPA, root directory `crm`, rewrite to `index.html`) |
| Local URL | http://localhost:3001 |

## Back end — Visa Consultancy API

| Item | Detail |
|------|--------|
| Location | `visaconsultantcrm-backend/` |
| Framework | **FastAPI 0.110.1** + Uvicorn 0.25 |
| Language | **Python 3.11** |
| Validation | **Pydantic v2** |
| Database | **MongoDB** via Motor 3.3 / PyMongo 4.6 |
| Auth | JWT HS256 (`python-jose` / PyJWT), bcrypt, TOTP (`pyotp`) |
| Tenancy | `tenant_id` on JWT and documents (default `tenant_default`) |
| File storage | Local disk or **S3-compatible** (Cloudflare R2) |
| Payments | **Razorpay** or mock |
| Email | **Resend** |
| OCR | In-process **MRZScanner** (DocsaidLab) + ICAO TD3; **PaddleOCR** for VIZ issue date / MRZ fallback (not Paddle Billing, not cloud ID APIs) |
| Hosting | **GCP Cloud Run** service `passage-api`, project `amaravisa-hub`, region `asia-south1` |
| Local URL | http://localhost:8000 |
| Health | `GET /api/health` |

Other notable libraries: `boto3`, `firebase-admin`, `cryptography` (Fernet PII), `python-multipart`, `opencv-python-headless`, `pymupdf`.

## What is not in the stack

- No Payload CMS
- No separate DASH backend
- No Stripe / Paddle Billing
- Parent folder `amaravisa` is a workspace only; Git remotes are the two repos above
