# Payloads and models

Source: `visaconsultantcrm-backend/models.py` and a few route-local Pydantic models. Optional fields are marked `?`. Enums are listed as allowed values.

Machine-readable JSON Schema for many of these is in [`openapi/openapi.json`](openapi/openapi.json) under `components.schemas`.

## Auth

### CustomerRegisterIn
`email` (email), `password` (min 6), `full_name`, `phone?`

### CustomerVerifyOtpIn
`pending_token`, `code` (exactly 6 characters)

### CustomerResendOtpIn
`pending_token`

### LoginIn
`email`, `password`

### CustomerGoogleIn
`id_token` (min 10), `mode`: `login` | `signup` (default `login`)

### CustomerForgotPasswordIn
`email`

### CustomerForgotPasswordResetIn
`email`, `code` (6), `new_password` (min 6)

### Verify2FAIn
`temp_token`, `code` (6)

### TwoFactorCodeIn
`code` (6)

### TwoFactorGenerateIn
`issuer?`

### Staff login success
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "staff@example.com",
    "full_name": "Name",
    "role": "admin",
    "role_name": "Admin",
    "menu_keys": ["dashboard", "role_master"],
    "unrestricted_scope": true,
    "country_codes": [],
    "two_factor_enabled": false
  }
}
```

Customer login returns `access_token`, `token_type`, `user` with `id`, `email`, `full_name` (no menu keys).

## Staff / roles

### StaffCreateIn
`email`, `password` (min 6), `full_name`, `role` (slug, default `consultant`), `country_codes[]`, `manager_id?`

Non-admin roles require at least one country code.

### StaffUpdateIn
`email`, `full_name`, `role`, `country_codes[]`, `manager_id?`, `password?` (min 6 if set)

### RoleCreateIn
`name`, `slug` (`^[a-z][a-z0-9-]{1,62}$`), `menu_keys[]`

`unrestricted_scope` is always false on create.

### RoleUpdateIn
`name?`, `menu_keys?`, `active?`

### StaffManagerIn
`manager_id?`

### BulkReassignIn
`to_consultant_id`, `country_code?`

### ReassignTargetIn
`target_consultant_id`

### ReassignCountriesIn
`target_consultant_id`, `new_country_codes[]`

### StaffProfileIn
`full_name?`

### ChangePasswordIn
`current_password`, `new_password` (min 6), `confirm_password` (min 6)

### CaseNumberFormatIn
`segments[]` (1–12) each:
- `type`: `FIXED` | `DATE` | `SERIAL`
- `fixed_text?`
- `date_format?`: `DD` | `MM` | `YY` | `YYYY` | `Mmm` | `MMM`
- `width?`
- `reset_interval?`: `""` | `DAILY` | `MONTHLY` | `YEARLY`

## Customer profile and travelers

### CustomerProfileIn (`PATCH /api/customers/me`)
`full_name?`, `phone?`, `dob?` (YYYY-MM-DD), `anniversary_date?`

### TravelerProfileIn
`full_name`, `relationship` (`self` | `spouse` | `child` | `parent` | `other`), `dob?`, `passport_number?`, `passport_issue_date?`, `passport_expiry_date?`, `gender?`, `nationality?`, `phone?`, `email?`

Passport numbers are encrypted at rest and masked on list.

## Catalog

### VisaProductIn
`country_code`, `country_name`, `visa_type` (`tourist` | `business` | `transit` | `other_general`), `visa_format?` (`visa_free` | `visa_on_arrival` | `e_visa` | `sticker_visa`), `title`, `banner_image_url?`, `validity_days`, `processing_time_days`, `passport_min_validity_months?` (default 6), `display_order?`

### VisaProductDocumentIn / PassportProductDocumentIn
`doc_key`, `doc_name?`, `description?`, `required?`, `formats_allowed?` (`pdf` | `jpg` | `png`), `max_file_size_mb?`, `sample_file_url?`, `display_order` (default 0)

### VisaProductFieldIn / PassportProductFieldIn
`field_key`, `label?`, `field_type?` (`text` | `date` | `dropdown` | `number` | `file`), `required?`, `options?`, `validation_regex?`, `display_order`

### VisaProductFeesIn / PassportProductFeesIn
`govt_fee`, `service_fee`, `currency` (default `INR`)

### PassportProductIn
`title`, `passport_service_type` (`fresh` | `reissue` | `damaged` | `lost` | `minor` | `tatkal`), `processing_time_days` (default 7), `banner_image_url?`

### ReorderItemIn
`id`, `display_order`

### DocumentMasterIn
`default_name`, `default_description?`, `default_formats_allowed[]` (default pdf/jpg/png), `default_max_file_size_mb` (10), `default_required` (true), `vault_eligible` (false), `is_basic` (false), `category?` (`identity` | `financial` | `travel` | `other`), `active` (true)

`doc_key` is generated server-side.

### FieldMasterIn
`default_label`, `default_field_type` (default `text`), `default_options?`, `default_required`, `validation_regex?`, `is_basic`, `active`

## Cases

### CaseDraftIn
`visa_product_id`, `traveler` (object), `field_values` (object), `document_uploads[]` (`doc_key`, `file_url`, `filename`)

### CaseDraftPatchIn
same optional fields plus `step?`

### MockCheckoutIn
`draft_id`, `outcome`: `success` | `failure`

### PaymentConfirmIn
`draft_id`, `order_id?`, `payment_id?`, `signature?`, `outcome`: `success` | `failure`

### OfflineCaseIn
`visa_product_id`, `customer_email`, `customer_full_name`, `customer_phone?`, `traveler`, `field_values`, `document_uploads[]`, `payment_status` (`pending` | `paid`), `payment_method?`, `payment_reference?`

### StageChangeIn
`target_stage` (`new` | `docs_pending` | `ready_to_submit` | `submitted` | `decision` | `closed`), `note?`

### DocumentVerifyIn
`note?`

### DocumentRejectIn
`reason`

### DocumentResubmitIn
`file_url`, `filename`

### ReassignIn
`consultant_id`

### DecisionIn
`outcome`: `approved` | `rejected` | `rfi`, `note?`

### TaskIn
`case_id?`, `description`, `due_date?`, `assigned_to?`, `priority`: `low` | `normal` | `high`, `category?`

### BulkCasesIn
`case_ids[]`, `action`: `reassign` | `stage`, `consultant_id?`, `target_stage?`

### CaseNoteIn
`body`

### CaseFieldEditIn
`field_key`, `value`

### PassportRenewalCaseIn
`customer_id`, `passport_number?`, `traveler_name?`, `passport_expiry_date?`, `preferred_service?` (default `reissue`), `passport_product_id?`

Case stages move `new` → `docs_pending` → `ready_to_submit` → `submitted` → `decision` → `closed`.

## Leads and commercial

### LeadIn
`full_name`, `email?`, `phone?`, `alternative_phone?`, `city?`, `country_code?`, `visa_type?`, `source?`, `notes?`, `assigned_to?`, `status` (`new` | `contacted` | `qualified` | `converted` | `lost`), `service_type` (`visa` | `passport` | `hotel_booking` | `ticket` | `package` | `travel_insurance` | `car_booking`), `service_details` (object), `lead_group_id?`, `language_preference?`, `lead_value` (default 0)

`service_details` shapes:

- **visa:** `visa_product_id?`, `adults`, `children`, `infants`, `country_code?`, `visa_type?`, fees, `gst_percent`, `total_amount?`, `refusal_faced`, `refusal_details?`
- **passport:** `passport_product_id?`, `passport_service_type?`, `applicants_count`, fees
- **hotel_booking:** `destination?`, `check_in?`, `check_out?`, `rooms`, `guests`, `budget?`, `notes?`
- **ticket:** `trip_type?`, `origin?`, `destination?`, `destination_country_code?`, `departure_date?`, `return_date?`, `passengers`, `budget?`, `notes?`
- **package:** `destination?`, `destination_country_code?`, `travel_date?`, `duration_days?`, `travelers`, `budget?`, `notes?`
- **travel_insurance:** `destination_country_code?`, `travel_start?`, `travel_end?`, `travelers`, `coverage_amount?`, `budget?`, `notes?`
- **car_booking:** `pickup_location?`, `drop_location?`, `pickup_date?`, `drop_date?`, `car_type?`, `budget?`, `notes?`

### LeadBatchCreateIn
Shared contact fields plus `services[]` (`service_type` + `service_details`), min 1 service.

### LeadConvertIn
`visa_product_id?`, `passport_product_id?`, `traveler?`, `service_details?`, `create_case` (true), `create_order` (true)

### LeadFollowUpIn
`contacted_at?`, `channel` (`phone` | `whatsapp` | `email` | `in_person` | `other`), `outcome` (`follow_up` | `callback` | `no_answer` | `switched_off` | `interested` | `not_interested` | `wrong_number` | `invalid` | `converted`), `notes?`, `next_follow_up_at?`, `forced_status?`

### AppointmentIn
`lead_id?`, `case_id?`, `customer_id?`, `scheduled_at`, `duration_minutes` (30), `mode` (`in_person` | `phone` | `video`), `notes?`, `assigned_to?`

### QuotationIn
`lead_id?`, `case_id?`, `customer_id?`, `country_code?`, `visa_product_id?`, `line_items[]`, `currency` (`INR`), `notes?`

### InvoiceIn
`case_id?`, `customer_id?`, `quotation_id?`, `amount`, `currency`, `due_date?`, `notes?`, `line_items[]`

### PaymentLedgerIn
`amount`, `payment_type` (`payment` | `refund`), `method?`, `reference?`, `notes?`

### CommunicationIn
`case_id?`, `lead_id?`, `customer_id?`, `channel` (`email` | `whatsapp` | `sms` | `call` | `portal` | `other`), `direction` (`inbound` | `outbound`), `subject?`, `body`, `status?` (default `logged`)

### QaReviewIn
`case_id`, `checklist[]`, `notes?`, `outcome?` (`pass` | `fail` | `needs_correction`)

### ServiceOrderStageIn
`target_stage` (`new` | `in_progress` | `completed` | `cancelled`), `note?`

### ServiceOrderReassignIn
`consultant_id`

### BulkServiceOrdersIn
`order_ids[]`, `action` (`reassign` | `stage`), `consultant_id?`, `target_stage?`

## Uploads

### `POST /api/documents/upload` and `/staff-upload`
`multipart/form-data` field `file`. Optional query `doc_key`. Returns a signed `file_url`.

### `POST /api/documents/scan-passport`
`multipart/form-data` field `file` (JPG/PNG/WebP/PDF). Customer JWT. Response includes `full_name`, `passport_number`, dates, `gender`, `nationality`, `ocr_confidence`, `request_id`, `warnings`.

### `POST /api/media/product-banner`
Staff JWT. Multipart image. Requires public R2 bucket config. Returns a public WebP URL.

### Razorpay webhook
`POST /api/cases/webhooks/razorpay` — raw JSON, header `X-Razorpay-Signature`. No Bearer token.
