# Release note — Apply continue React hooks fix

**Date:** 5 October 2026  
**Audience:** AmaraVisa engineering and operations

## What changed

Continuing a saved application from **My account** no longer crashes with React error #310 (“Something went wrong”).

## Cause

Cashfree payment-return hooks (`useRef` / `useEffect`) were declared after the apply page’s loading early-return. Resume with `?draft=` always starts with `draftLoaded=false`, so the first render skipped those hooks and the next render added them — a Rules-of-Hooks violation.

## Fix

Those hooks always run at the top of `ApplyPageInner`. Verify still waits until the product and draft are loaded, and calls finish-checkout through a ref.

## For applicants

- **Continue** on a draft opens the apply wizard again instead of the error screen.
- Cashfree return URLs (`cashfree_order_id` + `draft_id`) still confirm payment after load.

## Surfaces

- Customer: `visaconsultantcrm-frontend/customer/src/app/apply/[productId]/apply-inner.js`
- No API or payload changes.
