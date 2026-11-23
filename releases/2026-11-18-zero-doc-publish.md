# Zero-document product publish

**Date:** 18 Nov 2026

## What changed

CRM Product Builder can **Publish** visa and passport products that have **no required documents** (and even no document slots at all). Pricing (`govt_fee` / `service_fee`) and processing time remain mandatory.

This matches the customer site: `/apply` already skips the Documents step when `schema.documents` is empty.

## Why

Publish previously failed with `At least one required document is needed` from `can_publish()`, even though apply/catalog already supported zero-doc products (e.g. MDAC-style).

## APIs

| Method | Path | Notes |
|--------|------|--------|
| `GET` | `/api/admin/visa-products/{id}/can-publish` | Returns `{ ok, errors[] }` — no longer errors on 0 required docs |
| `PATCH` | `/api/admin/visa-products/{id}/publish` | Same gate |
| `GET` / `PATCH` | `/api/admin/passport-products/{id}/can-publish` / `publish` | Shared `can_publish(..., product_type="passport")` |

See [02-architecture-and-integration.md](../02-architecture-and-integration.md).
