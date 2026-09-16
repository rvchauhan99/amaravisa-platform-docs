# API catalog — CRM / DASH (`/api/crm`)

These endpoints power the **staff CRM**. All require a staff JWT (`Authorization: Bearer`). Several also require a Role Master menu key (see [03-authentication-and-rbac.md](03-authentication-and-rbac.md)).

Interactive docs: [Swagger UI](http://127.0.0.1:8000/docs) · snapshot in [`openapi/openapi.json`](openapi/openapi.json).


**71 operations** in this catalog.

## crm_commercial

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/appointments` | staff JWT (+ menu where noted) |  |  | List Appointments |
| POST | `/api/crm/appointments` | staff JWT (+ menu where noted) | AppointmentIn |  | Create Appointment |
| PATCH | `/api/crm/appointments/{appointment_id}/status` | staff JWT (+ menu where noted) | AppointmentStatusIn |  | Patch Appointment Status |
| GET | `/api/crm/communications` | staff JWT (+ menu where noted) |  | case_id, lead_id, channel, direction, status, q, from_date, to_date, page, limit, sort_by, sort_order | List Communications |
| POST | `/api/crm/communications` | staff JWT (+ menu where noted) | CommunicationIn |  | Create Communication |
| GET | `/api/crm/invoices` | staff JWT (+ menu where noted) |  | status, case_id, overdue, amount_min, amount_max, from_date, to_date, due_from, due_to, q, page, limit, sort_by, sort_order | List Invoices |
| POST | `/api/crm/invoices` | staff JWT (+ menu where noted) | InvoiceIn |  | Create Invoice |
| POST | `/api/crm/invoices/{invoice_id}/payments` | staff JWT (+ menu where noted) | PaymentLedgerIn |  | Add Invoice Payment |
| GET | `/api/crm/lead-follow-ups` | staff JWT (+ menu where noted) |  | status, source, country, assigned_to, visa_type, service_type, outcome, channel, due, q, from_date, to_date, next_from, next_to, contacted_from, contacted_to, page, limit, sort_by, sort_order | List Lead Follow Up Queue |
| GET | `/api/crm/lead-follow-ups/counts` | staff JWT (+ menu where noted) |  |  | Lead Follow Up Counts |
| GET | `/api/crm/leads` | staff JWT (+ menu where noted) |  | status, source, country, assigned_to, visa_type, service_type, outcome, due, q, from_date, to_date, next_from, next_to, contacted_from, contacted_to, page, limit, sort_by, sort_order | List Leads |
| POST | `/api/crm/leads` | staff JWT (+ menu where noted) | LeadIn |  | Create Lead |
| POST | `/api/crm/leads/batch` | staff JWT (+ menu where noted) | LeadBatchCreateIn |  | Create Leads Batch |
| GET | `/api/crm/leads/{lead_id}` | staff JWT (+ menu where noted) |  |  | Get Lead |
| PATCH | `/api/crm/leads/{lead_id}` | staff JWT (+ menu where noted) | LeadPatchIn |  | Patch Lead |
| POST | `/api/crm/leads/{lead_id}/convert` | staff JWT (+ menu where noted) | LeadConvertIn |  | Convert Lead |
| GET | `/api/crm/leads/{lead_id}/follow-ups` | staff JWT (+ menu where noted) |  |  | List Lead Follow Ups |
| POST | `/api/crm/leads/{lead_id}/follow-ups` | staff JWT (+ menu where noted) | LeadFollowUpIn |  | Create Lead Follow Up |
| GET | `/api/crm/leads/{lead_id}/group` | staff JWT (+ menu where noted) |  |  | Get Lead Group |
| GET | `/api/crm/qa-reviews` | staff JWT (+ menu where noted) |  |  | List Qa Reviews |
| POST | `/api/crm/qa-reviews` | staff JWT (+ menu where noted) | QaReviewIn |  | Create Qa Review |
| PATCH | `/api/crm/qa-reviews/{review_id}/outcome` | staff JWT (+ menu where noted) | QaReviewOutcomeIn |  | Patch Qa Outcome |
| GET | `/api/crm/quotations` | staff JWT (+ menu where noted) |  | status, case_id, q, from_date, to_date, page, limit, sort_by, sort_order | List Quotations |
| POST | `/api/crm/quotations` | staff JWT (+ menu where noted) | QuotationIn |  | Create Quotation |
| PATCH | `/api/crm/quotations/{quotation_id}/status` | staff JWT (+ menu where noted) | QuotationStatusIn |  | Patch Quotation Status |

## crm_extras

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/birthdays` | staff JWT (+ menu where noted) |  | within | Birthdays Dashboard |
| GET | `/api/crm/notifications` | staff JWT (+ menu where noted) |  | unread_only | Staff Notifications |
| POST | `/api/crm/notifications/mark-all-read` | staff JWT (+ menu where noted) |  |  | Mark All Read |
| GET | `/api/crm/notifications/unread-count` | staff JWT (+ menu where noted) |  |  | Unread Count |
| GET | `/api/crm/passport-expiry` | staff JWT (+ menu where noted) |  | days | Passport Expiry Dashboard |
| POST | `/api/crm/passport-expiry/renewal-case` | staff JWT (+ menu where noted) | PassportRenewalCaseIn |  | Create Passport Renewal Case |

## crm

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/case-groups/{group_id}` | staff JWT (+ menu where noted) |  |  | Get Case Group |
| GET | `/api/crm/cases` | staff JWT (+ menu where noted) |  | stage, stage_group, country, consultant_id, sla, source, payment_status, on_hold, unassigned, decision, visa_type, case_type, q, from_date, to_date, closed_from, closed_to, page, limit, sort_by, sort_order, include_summary, include_docs | List Cases |
| POST | `/api/crm/cases` | staff JWT (+ menu where noted) | OfflineCaseIn |  | Create Offline Case |
| POST | `/api/crm/cases/bulk` | staff JWT (+ menu where noted) | BulkCasesIn |  | Bulk Cases |
| GET | `/api/crm/cases/{case_id}` | staff JWT (+ menu where noted) |  |  | Case Detail |
| POST | `/api/crm/cases/{case_id}/decision` | staff JWT (+ menu where noted) | DecisionIn |  | Record Decision |
| POST | `/api/crm/cases/{case_id}/documents/{doc_id}/reject` | staff JWT (+ menu where noted) | DocumentRejectIn |  | Reject Doc |
| POST | `/api/crm/cases/{case_id}/documents/{doc_id}/verify` | staff JWT (+ menu where noted) | DocumentVerifyIn |  | Verify Doc |
| PATCH | `/api/crm/cases/{case_id}/fields` | staff JWT (+ menu where noted) | CaseFieldEditIn |  | Edit Field Value |
| POST | `/api/crm/cases/{case_id}/notes` | staff JWT (+ menu where noted) | CaseNoteIn |  | Add Note |
| PATCH | `/api/crm/cases/{case_id}/reassign` | staff JWT (+ menu where noted) | ReassignIn |  | Reassign Case |
| PATCH | `/api/crm/cases/{case_id}/stage` | staff JWT (+ menu where noted) | StageChangeIn |  | Change Stage |
| GET | `/api/crm/consultants` | staff JWT (+ menu where noted) |  | country, q, limit, offset, id | List Consultants |
| GET | `/api/crm/ops/queues` | staff JWT (+ menu where noted) |  |  | Ops Queues |
| GET | `/api/crm/search` | staff JWT (+ menu where noted) |  | q | Crm Search |
| POST | `/api/crm/tasks` | staff JWT (+ menu where noted) | TaskIn |  | Create Task |
| GET | `/api/crm/tasks/my` | staff JWT (+ menu where noted) |  | status, priority, category, due, from_date, to_date, assigned_to, q, page, limit, sort_by, sort_order | My Tasks |
| PATCH | `/api/crm/tasks/{task_id}/done` | staff JWT (+ menu where noted) |  |  | Close Task |
| GET | `/api/crm/workload` | staff JWT (+ menu where noted) |  |  | Workload |

## crm_clients

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/clients` | staff JWT (+ menu where noted) |  | q, page, limit, sort_by, sort_order, service_type, has_work, has_open_work | Clients List |
| GET | `/api/crm/clients/{customer_id}` | staff JWT (+ menu where noted) |  |  | Client Detail |
| GET | `/api/crm/clients/{customer_id}/analytics` | staff JWT (+ menu where noted) |  |  | Client Analytics Route |
| GET | `/api/crm/clients/{customer_id}/history` | staff JWT (+ menu where noted) |  | kind, status, from_date, to_date, page, limit | Client History Route |

## payments

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/payments` | staff JWT (+ menu where noted) |  | from_date, to_date, method, payment_type, case_id, invoice_id, country, consultant_id, q, page, limit, sort_by, sort_order | List Payments |
| GET | `/api/crm/reports/payments` | staff JWT (+ menu where noted) |  | from_date, to_date, method, payment_type, country, consultant_id | Payments Summary |
| GET | `/api/crm/reports/payments/export.csv` | staff JWT (+ menu where noted) |  | from_date, to_date, method, payment_type, country, consultant_id | Payments Export Csv |
| GET | `/api/crm/reports/receivables` | staff JWT (+ menu where noted) |  | from_date, to_date, status, country, consultant_id | Receivables Report |

## reports_dashboard

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/reports/dashboard` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id, stage, sla, payment_status, on_hold, unassigned, decision, visa_type, case_type, service_type, q, granularity | Dashboard Report |

## reports

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/reports/doc-rejection-rate` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id | Doc Rejection Rate |
| GET | `/api/crm/reports/export.csv` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id, stage_group, stage, decision, visa_type, payment_status, closed_from, closed_to, q | Export Csv |
| GET | `/api/crm/reports/funnel` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id | Funnel Report |
| GET | `/api/crm/reports/pipeline` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id | Pipeline Report |
| GET | `/api/crm/reports/revenue` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id | Revenue Report |
| GET | `/api/crm/reports/sla` | staff JWT (+ menu where noted) |  | from_date, to_date, country, source, consultant_id | Sla Report |

## reports_leads

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/reports/leads` | staff JWT (+ menu where noted) |  | status, source, country, assigned_to, visa_type, service_type, outcome, due, q, from_date, to_date, next_from, next_to, granularity | Leads Analytics |

## service_orders

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/crm/service-orders` | staff JWT (+ menu where noted) |  | status, service_type, assigned_to, q, from_date, to_date, page, limit, sort_by, sort_order | List Service Orders |
| POST | `/api/crm/service-orders/bulk` | staff JWT (+ menu where noted) | BulkServiceOrdersIn |  | Bulk Service Orders |
| GET | `/api/crm/service-orders/{order_id}` | staff JWT (+ menu where noted) |  |  | Get Service Order |
| PATCH | `/api/crm/service-orders/{order_id}/reassign` | staff JWT (+ menu where noted) | ServiceOrderReassignIn |  | Reassign Service Order |
| PATCH | `/api/crm/service-orders/{order_id}/stage` | staff JWT (+ menu where noted) | ServiceOrderStageIn |  | Change Service Order Stage |

## Menu keys (CRM / admin)

- `/api/crm/cases*`: `pipeline` for list/detail; `offline_case` for POST create; `tasks` for task routes
- `/api/crm/reports/dashboard*`: `dashboard`
- `/api/crm/reports/leads*`: `lead_analytics`
- `/api/crm/reports/payments*`: `payment_reports`
- `/api/crm/payments*`: `payment_reports`
- `/api/crm/birthdays*`: `birthdays`
- `/api/crm/passport-expiry*`: `passport_expiry`
- `/api/crm/clients*`: `clients`
- `/api/crm/service-orders*`: `service_orders`
- `/api/crm/reports/pipeline*`: `case_reports`

Leads, follow-ups, finance, inbox, appointments, quotations, invoices, and communications currently use **staff JWT only** (country/hierarchy scope). The CRM sidebar still hides those pages unless the role has the matching menu key.
