# Customer response shapes

**Canonical Out shapes** for the customer site. Request bodies stay in [07-payloads-and-models.md](07-payloads-and-models.md). Dummy JSON: [openapi/api-examples.json](openapi/api-examples.json).

Field lists below are required for binding; extra keys may appear — ignore unknown keys safely.

---

## Product list — `GET /api/visa-products`

Response is a paginated object with `items[]` (and paging fields as implemented). Each **list item** includes at least:

| Field | Notes |
|-------|--------|
| `id` | Same as `visa_product_id` on detail |
| `title`, `country_code`, `country_name`, `country_flag` | |
| `visa_type`, `visa_format` | |
| `validity_days`, `processing_time_days` | From default plan |
| `fees` | `{ govt_fee, service_fee, currency }` |
| `from_price` | Catalog “from” price when present |
| `variant_count` | `> 1` → multi-SKU |
| `variants[]` | Compact plan rows (see variant shape) |
| `documents_profile`, `required_documents_count`, `required_doc_keys` | Filters / badges |
| `banner_image_url`, `display_order`, `status` | |
| `complexity` | Optional catalog facet |

---

## Product detail — `GET /api/visa-products/{product_id}`

Query: `variant_id?` overlays fees / validity / processing for that plan.

| Field | Notes |
|-------|--------|
| `visa_product_id` | Use in apply / drafts |
| `product_type` | e.g. `visa` |
| `title`, `country_*`, `visa_type`, `visa_format`, `banner_image_url` | |
| `status` | Customer only uses `published` |
| `validity_days`, `processing_time_days`, `max_stay_days`, `entry_type` | Active/default overlay |
| `passport_min_validity_months`, `passport_product_id` | |
| `fees` | Overlay for selected/default plan |
| `variant_id`, `variant`, `variant_count`, `variants[]` | Plans |
| `fixed_fields[]` | Always-collected traveler keys |
| `fields[]` | Custom: `field_key`, `label`, `type`, `required`, `options`, `order` |
| `documents[]` | `doc_key`, `name`, `required`, `formats`, `max_size_mb`, `sample_file_url`, `order`, `vault_eligible` |

### Variant row (`variants[]` and overlay `variant`)

| Field | Notes |
|-------|--------|
| `id` | Pass as `variant_id` |
| `visa_product_id` | |
| `label` | Display name |
| `validity_days`, `max_stay_days`, `entry_type`, `processing_time_days` | |
| `is_default`, `display_order`, `status` | Prefer `active` |
| `fees` | `{ govt_fee, service_fee, currency }` |

---

## Fee change log — `GET /api/visa-products/fee-change-log`

```json
{
  "country": { "code": "GBR", "name": "United Kingdom", "flag": "🇬🇧" },
  "items": [
    {
      "changed_at": "ISO-8601",
      "product_id": "...",
      "product_title": "...",
      "visa_type": "tourist",
      "variant_id": "...",
      "variant_label": "180 Days · Multi-entry",
      "fee_type": "service_fee",
      "from_amount": 7068.0,
      "to_amount": 7100.0,
      "difference": 32.0,
      "currency": "INR",
      "reason": "..."
    }
  ]
}
```

`country` is `null` when search does not resolve. UI may hide `product_*` columns; show **Plan** from `variant_label`.

---

## Countries — `GET /api/visa-products/countries`

Array (or wrapped list) of `{ code, name, flag, ... }` for typeahead. Query: `q?`, `limit?`.

---

## Draft — `POST /api/cases` / `GET|PATCH /api/cases/drafts/{id}`

Draft document includes at least:

| Field | Notes |
|-------|--------|
| `id` | Draft id (`?draft=`) |
| `visa_product_id`, `variant_id` | |
| `customer_id`, `tenant_id` | |
| `travelers[]` | Party members with `id`, fields, uploads |
| `step`, `active_traveler_id` | Wizard position |
| `case_group_id?` | Set on multi-traveler checkout |

Create response includes `draft_id` (and often `variant_id`, `traveler_count`).

---

## Create order — `POST /api/cases/checkout/create-order`

Body: `{ draft_id, outcome? }`.

Response includes:

| Field | Notes |
|-------|--------|
| `mode` / payment mode | `bank_transfer` or cashfree-related |
| `order_id` | Synthetic bank id or gateway id |
| `currency`, amounts | |
| `traveler_count`, `unit_amount`, `total_amount` | |
| `payment_session_id`, `cashfree_env` | Present when Cashfree configured |

Wait for this before rendering Payment UI ([10](10-customer-apply-and-checkout.md)).

Cashfree-specific: `POST .../cashfree/create-order` → session payload; `POST .../cashfree/verify` → checkout success shape.

---

## Checkout success — `POST /api/cases/checkout` (and Cashfree verify)

| Field | Notes |
|-------|--------|
| `status` | `success` |
| `case_id` / `primary_case_id` | Navigate to `/status/{case_id}` |
| `case_ids[]` | All travelers |
| `case_group_id` | Family booking |
| `traveler_count` | |
| `payment_mode` | `bank_transfer` \| `cashfree` \| … |
| `payment_status` | `pending` \| `paid` |

---

## Case status — `GET /api/cases/{case_id}/status`

Includes case core fields plus:

| Field | Notes |
|-------|--------|
| `payment_status`, `payment_proof`, `payment_proof_rejection` | Bank flow |
| `sibling_cases[]` / group helpers | Family UI |
| Stage / document status fields | As returned by API |

Receipt: `GET /api/cases/{case_id}/receipt` when paid.

---

## Account

| Endpoint | Shape notes |
|----------|-------------|
| `GET /api/customers/me` | Profile |
| `GET /api/customers/me/traveler-profiles` | List / CRUD profiles |
| `GET /api/customers/me/document-vault` | Vault items |
| `GET /api/cases/my` | Applications (may include `case_group_id`) |
| `GET /api/cases/drafts` | Resume drafts |
| `GET /api/customers/me/notifications` | Portal notifications |

---

## Bank details — `GET /api/payment/bank-details`

Customer JWT. `{ bank_name, account_name, account_number, ifsc, branch_name, upi_id }` — any may be `null`. Empty `upi_id` → hide QR.

---

## Spot-check (local)

```bash
curl -sS http://localhost:8000/api/visa-products/1ed86e5a-3b22-4991-aa4d-38b4fb528814 | jq 'keys'
curl -sS 'http://localhost:8000/api/visa-products/fee-change-log?search=GBR' | jq '.items[0]'
```
