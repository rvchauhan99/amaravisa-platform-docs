# 2026-11-05 — Brand name lowercase (amaravisa)

**Audience:** amaravisa engineering, marketing, and operations

## What changed

The marketing brand string is now always lowercase **amaravisa** across the customer site (titles, meta/OG, copy), CRM chrome, transactional emails, 2FA issuer label, and partner docs.

## Unchanged (by design)

- Bank payment account name remains **AMARAVISA INDIA PRIVATE LIMITED**
- Legal entity display remains **AmaraVisa India Private Limited** (footer, schema.org `legalName`)

## Surfaces

| Surface | Effect |
|---------|--------|
| Customer Next.js | `SITE_NAME`, page titles, keywords, FAQ/footer brand copy |
| CRM | Document title, login/layout brand, logo component rename |
| API emails / 2FA | Resend display name examples, email shell, `DEFAULT_2FA_ISSUER` |
| Docs | Catalogs/examples issuer strings, this release note |

## Ops note

If production `RESEND_FROM` still uses the old display name, update it to `amaravisa <…>` when convenient so outbound mail matches the site.
