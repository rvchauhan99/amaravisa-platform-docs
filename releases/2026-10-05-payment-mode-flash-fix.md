# 2026-10-05 — Payment mode UI flash fix

## Summary

On `/apply` Payment, the bank-transfer receipt uploader no longer flashes while checkout mode is still loading. Cashfree shows only after `create-order` returns `mode=cashfree`.

## Change

`PaymentStep` waits for `POST /api/cases/checkout/create-order` before rendering either Cashfree Pay or the receipt upload / Submit application UI. While loading, only “Checking payment options…” is shown.

## Verify

- Cashfree configured: Checking… → Pay (no Payment receipt flash)
- Cashfree unset: Checking… → receipt upload + Submit application
