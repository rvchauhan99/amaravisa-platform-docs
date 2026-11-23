# Fee reason minimum-character guideline (CRM)

**Date:** 23 Nov 2026

## What changed

Visa Product Builder **Pricing** tab now shows a live guideline under **Reason for fee change**:

- Short / empty: `Minimum 10 characters (N/10)`
- Valid: `Ready (N/10)`

**Save new pricing** stays disabled until the trimmed reason is at least **10 characters** (same rule as `VisaProductFeesIn.reason` on the API).

## Why

Staff saw a grey Save button with no explanation of the minimum length.

## Surfaces

| Surface | Notes |
|---------|--------|
| CRM `/products/:id` Pricing | Live count + toast mentions min 10 |
| `POST /api/admin/visa-products/{id}/fees` | Unchanged: `reason` min_length 10 |

See [02-architecture-and-integration.md](../02-architecture-and-integration.md).
