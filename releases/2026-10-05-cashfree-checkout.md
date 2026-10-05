# Release note — Cashfree checkout

**Date:** 5 October 2026
**Audience:** AmaraVisa operations and leadership

## What changed

Card, UPI, and netbanking checkout can run through Cashfree. Bank transfer stays the live checkout until both Cashfree API keys are set on the API.

## For applicants

- With Cashfree keys set, the Payment step shows **Pay** and opens Cashfree Checkout. A transfer receipt is not required.
- The application is created as paid only after Cashfree reports the order as paid.
- A phone number on the traveler is required to start that payment.
- Without the keys, the existing HDFC transfer and receipt upload stay as they are.

## For staff

- Cashfree payments arrive already marked paid. Staff do not confirm a UTR for those cases.
- Bank-transfer cases still wait for **Confirm payment** on the case Payment tab.

## API

- Cashfree orders use API version `2025-01-01`. `CASHFREE_APP_ID` and `CASHFREE_SECRET_KEY` are accepted as aliases for the client id and secret.
- `POST /api/cases/checkout/cashfree/create-order` and `POST /api/cases/checkout/cashfree/verify` are the apply-page calls.
- `POST /api/cases/checkout/create-order` also returns `payment_session_id` and `cashfree_env` when Cashfree is on.
- `POST /api/cases/checkout` confirms a Cashfree `order_id`.
- `POST /api/cases/webhooks/cashfree` accepts `PAYMENT_SUCCESS_WEBHOOK` (`x-webhook-signature`, `x-webhook-timestamp`).
