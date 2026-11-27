# Fee change transparency (customer site)

**Date:** 8 Nov 2026

## What customers see

Public page **`/transparency/price-change-log`** (exact Atlys fee-change UI/UX parity; amaravisa brand):

- Search a destination (“Where to”) by country name or ISO-3 code (e.g. `VNM`)
- Table columns: Date, **Plan** (`variant_label` or `—`), Fee Type (Service / Government pills), From, To, Difference, Reason — Product is not shown (API may still return `product_*` for internal use)
- Linked from the footer (**Fee change history**) and from the visa detail fee card
- Visa product master is unchanged except append-only fee rows + required public `reason` on plan fee save
- Fee streams are **per plan (`variant_id`)**; UI **Plan** column shows `variant_label`

## How fees are tracked

CRM Product Builder **Plans & pricing** (not a separate Pricing tab) requires a **public reason** (min 10 characters) on every fee save. Each save appends a new `visa_product_fees` row (`reason`, `created_by`, `variant_id`). The public API diffs consecutive versions **per variant stream** and emits one row per changed fee type.

Legacy fee rows without a stored reason display **Fee schedule updated**.

## APIs

| Method | Path | Notes |
|--------|------|--------|
| `GET` | `/api/visa-products/fee-change-log` | Public; `country` / `search` / `q` |
| `POST` | `/api/admin/visa-products/{id}/fees` | Body now requires `reason` |

See [02-architecture-and-integration.md](../02-architecture-and-integration.md) and [07-payloads-and-models.md](../07-payloads-and-models.md).
