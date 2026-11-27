# 2026-11-27 — Visa product variants (multi-validity / multi-price)

**Non-breaking / opt-in.** Existing single-SKU admin Product Builder and customer browse → apply → checkout paths keep working.

## What changed

- New collection `visa_product_variants` with silent migration `015` creating one **default active** variant per existing product and backfilling `variant_id` on fee rows.
- Fees remain append-only; `POST .../fees` without `variant_id` targets the default variant.
- Admin CRM **Plans & pricing** tab (testid `variants`) is the sole fee/SKU editor; the separate Pricing tab was removed (see [plans-pricing-admin](2026-11-27-plans-pricing-admin.md)).
- Customer detail shows an Atlys-style picker only when `variant_count > 1`; otherwise the previous UI is unchanged.
- Customer variant group cards use a focusable `div` (not a nested `<button>`) so processing chips stay valid HTML and avoid hydration errors.
- Drafts accept optional `variant_id` (server defaults when omitted). Case snapshots keep flat `fees` / `validity_days` and add an optional `variant` object.
- Local seed expands UK Visitor into multi-validity demo SKUs when still single-variant.

## Docs

- Payloads: `07-payloads-and-models.md`
- Admin catalog: variant CRUD routes in `06-api-catalog-admin.md`
- Customer catalog: `variant_id` query on product detail in `04-api-catalog-customer.md`
