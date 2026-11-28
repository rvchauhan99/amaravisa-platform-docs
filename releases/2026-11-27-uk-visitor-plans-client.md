# Client release note — Plans & pricing (platform-wide)

**Date:** 27 November 2026  
**Scope:** Entire amaravisa platform (all destinations)  
**Example used below:** UK Standard Visitor Visa  

---

## What changed (global)

amaravisa now supports **multiple plans under one visa product** for **any country**, not only the UK.

| Before | After |
|--------|--------|
| One validity / one processing / one price per product | Staff can add several plans on the same product |
| Customer saw a single fee card | If a product has more than one plan, customer sees a plan picker |
| Fees edited in a separate Pricing area | All plan fees live under CRM **Plans & pricing** |

This is a **platform-level** capability. UK is configured first as a full example. Other destinations stay on a single plan until you add more in admin — they keep working as today.

### Same fields for every destination

Each plan (any country) uses:

| Field (Plans & pricing) | Simple meaning |
|-------------------------|----------------|
| **Label** | Name shown to the customer |
| **Validity (days)** | How long the visa stays valid |
| **Max stay (days)** | Longest stay allowed per visit |
| **Entry** | `single` / `double` / `multiple` (Multi-entry = enter/leave many times while valid) |
| **Processing (days)** | Target delivery (“Visa in N days”) |
| **Government fee** | Govt / consulate fee (INR) |
| **Service fee** | amaravisa service fee (INR; GST added on the website) |
| **Default** | Pre-selected if the customer does not change the plan |

Rules that apply **everywhere**:

1. One product can have many plans; the customer still picks **one** plan per application.  
2. Same validity + entry + max stay with different processing = one category card with speed/price chips (like UK 180-day Standard vs Faster).  
3. Submitted applications keep the plan and fees the customer paid for.  
4. Fee changes need a public reason; **Fee change history** can show a **Plan** name.  
5. Products with only one plan look the same as before (no picker).

---

## Example — UK Standard Visitor Visa

**Product:** UK Standard Visitor Visa (GBR) · Tourist · Sticker visa  

One UK product, **five plans** on the same page (worked example of the global feature).

### 1. 180 Days · Multi-entry — Standard (default)

| Field | Value |
|-------|--------|
| Label | 180 Days · Multi-entry |
| Validity | 180 days (6 months) |
| Max stay | 180 days |
| Entry | Multiple |
| Processing | 38 days |
| Government fee | ₹18,322 |
| Service fee | ₹7,068 |
| Default | Yes |

Website total (GST on service): about **₹26,662**.

### 2. 180 Days · Multi-entry — Faster

Same category as plan 1; only processing and price differ.

| Field | Value |
|-------|--------|
| Label | 180 Days · Multi-entry |
| Validity | 180 days |
| Max stay | 180 days |
| Entry | Multiple |
| Processing | 12 days |
| Government fee | ₹18,322 |
| Service fee | ₹92,838 |
| Default | No |

Website total (GST on service): about **₹1,27,871**.

### 3. 2 Years · Multi-entry

| Field | Value |
|-------|--------|
| Label | 2 Years · Multi-entry |
| Validity | 730 days (2 years) |
| Max stay | 180 days |
| Entry | Multiple |
| Processing | 47 days |
| Government fee | ₹69,325 |
| Service fee | ₹7,068 |
| Default | No |

Website total (GST on service): about **₹77,665**.

### 4. 5 Years · Multi-entry

| Field | Value |
|-------|--------|
| Label | 5 Years · Multi-entry |
| Validity | 1,825 days (5 years) |
| Max stay | 180 days |
| Entry | Multiple |
| Processing | 47 days |
| Government fee | ₹1,21,592 |
| Service fee | ₹11,799 |
| Default | No |

Website total (GST on service): about **₹1,35,515**.

### 5. 10 Years · Multi-entry

| Field | Value |
|-------|--------|
| Label | 10 Years · Multi-entry |
| Validity | 3,650 days (10 years) |
| Max stay | 180 days |
| Entry | Multiple |
| Processing | 47 days |
| Government fee | ₹1,56,609 |
| Service fee | ₹11,799 |
| Default | No |

Website total (GST on service): about **₹1,70,532**.

### UK quick view

| # | Label | Validity | Max stay | Entry | Process | Govt fee | Service fee | Default |
|---|--------|----------|----------|--------|---------|----------|-------------|---------|
| 1 | 180 Days · Multi-entry | 180 d | 180 d | Multiple | 38 d | ₹18,322 | ₹7,068 | Yes |
| 2 | 180 Days · Multi-entry | 180 d | 180 d | Multiple | 12 d | ₹18,322 | ₹92,838 | No |
| 3 | 2 Years · Multi-entry | 730 d | 180 d | Multiple | 47 d | ₹69,325 | ₹7,068 | No |
| 4 | 5 Years · Multi-entry | 1,825 d | 180 d | Multiple | 47 d | ₹1,21,592 | ₹11,799 | No |
| 5 | 10 Years · Multi-entry | 3,650 d | 180 d | Multiple | 47 d | ₹1,56,609 | ₹11,799 | No |

---

## Short message you can send

We have upgraded amaravisa **platform-wide** so any visa product can offer multiple plans (validity, max stay, entry type, processing days, government fee, and service fee) under **Plans & pricing**. Customers only see a plan picker when a product has more than one plan; single-plan destinations look the same as before.  

**UK Standard Visitor Visa** is the first full example: five plans on one page (180-day Multi-entry with 38-day or 12-day processing, plus 2 / 5 / 10 year Multi-entry). The same structure can be rolled out to other countries when you are ready.
