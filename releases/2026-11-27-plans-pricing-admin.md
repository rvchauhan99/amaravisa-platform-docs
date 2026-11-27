# 2026-11-27 — Plans & pricing admin (Pricing tab removed)

Visa Product Builder no longer has a separate **Pricing** tab. Fees and multi-validity SKUs live only under **Plans & pricing**.

## What changed

- CRM tabs: Basic · Documents · Fields · **Plans & pricing** (`data-testid="pb-tab-variants"`).
- **Update fees** on a plan: govt / service / public reason (min 10 chars) via `POST /api/admin/visa-products/{id}/variants/{variant_id}/fees`.
- **Edit plan**: label, validity, stay, entry, processing, order via `PATCH .../variants/{id}`.
- **Add plan**: create variant + initial fees in one flow.
- Multi-SKU products: Basic hides validity/processing; manage those on Plans & pricing.
- Single-SKU: Basic still syncs validity/processing to the default plan; fees still only on Plans & pricing.
- Customer fee-change log adds a **Plan** column (`variant_label`).
- Backend `POST .../fees` (default variant) kept for scripts/tests; CRM UI does not use it.

## Docs

- Architecture: `02-architecture-and-integration.md`
- Related: `2026-11-27-visa-product-variants.md`
