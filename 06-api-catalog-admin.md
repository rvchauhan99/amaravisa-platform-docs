# API catalog — admin, staff self-service, and catalog builders

User Master, Role Master, visa/passport product builders, case-number settings, staff 2FA, and `/staff/me`. Most require a staff JWT **and** a menu key.

Interactive docs: [Swagger UI](http://127.0.0.1:8000/docs) · snapshot in [`openapi/openapi.json`](openapi/openapi.json).


**68 operations** in this catalog.

## admin

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/admin/consultants` | staff JWT + menu |  | q, limit, offset, id | List All Consultants |
| POST | `/api/admin/consultants` | staff JWT + menu | StaffCreateIn |  | Create Consultant |
| GET | `/api/admin/consultants/audit` | staff JWT + menu |  | limit | List Staff Audit |
| PATCH | `/api/admin/consultants/{cid}` | staff JWT + menu | StaffUpdateIn |  | Update Consultant |
| PATCH | `/api/admin/consultants/{cid}/activate` | staff JWT + menu |  |  | Activate |
| GET | `/api/admin/consultants/{cid}/audit` | staff JWT + menu |  | limit | List Consultant Audit |
| PATCH | `/api/admin/consultants/{cid}/countries` | staff JWT + menu | array[string] |  | Update Countries |
| PATCH | `/api/admin/consultants/{cid}/deactivate` | staff JWT + menu |  |  | Deactivate |
| PATCH | `/api/admin/consultants/{cid}/manager` | staff JWT + menu | StaffManagerIn |  | Update Manager |
| POST | `/api/admin/consultants/{cid}/reassign-and-deactivate` | staff JWT + menu | ReassignTargetIn |  | Reassign And Deactivate |
| POST | `/api/admin/consultants/{cid}/reassign-and-update-countries` | staff JWT + menu | ReassignCountriesIn |  | Reassign And Update Countries |
| POST | `/api/admin/consultants/{cid}/reassign-open` | staff JWT + menu | BulkReassignIn |  | Bulk Reassign Open |
| GET | `/api/admin/settings/case-number-format` | staff JWT + menu |  |  | Get Case Number Format |
| PATCH | `/api/admin/settings/case-number-format` | staff JWT + menu | CaseNumberFormatIn |  | Update Case Number Format |
| GET | `/api/admin/settings/product-catalog-status` | staff JWT + menu |  |  | Get Product Catalog Status |

## masters

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/admin/document-master` | staff JWT + menu |  | active, q, limit, offset, id | List Document Master (`q` matches `doc_key`, `default_name`, `default_description`, `category`; omit `limit` for full list) |
| POST | `/api/admin/document-master` | staff JWT + menu | DocumentMasterIn |  | Create Document Master |
| PATCH | `/api/admin/document-master/{master_id}` | staff JWT + menu | DocumentMasterPatch |  | Patch Document Master |
| GET | `/api/admin/field-master` | staff JWT + menu |  | active, q, limit, offset, id | List Field Master (`q` matches `field_key`, `default_label`, `default_field_type`, options text, `validation_regex`; omit `limit` for full list) |
| POST | `/api/admin/field-master` | staff JWT + menu | FieldMasterIn |  | Create Field Master |
| PATCH | `/api/admin/field-master/{master_id}` | staff JWT + menu | FieldMasterPatch |  | Patch Field Master |

## passport_products

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/admin/passport-products` | staff JWT + menu |  | q, limit, offset, id | List Admin Passport Products |
| POST | `/api/admin/passport-products` | staff JWT + menu | PassportProductIn |  | Create Passport Product |
| GET | `/api/admin/passport-products/{product_id}` | staff JWT + menu |  |  | Get Admin Passport Product |
| PATCH | `/api/admin/passport-products/{product_id}` | staff JWT + menu | PassportProductIn |  | Update Passport Product |
| GET | `/api/admin/passport-products/{product_id}/can-publish` | staff JWT + menu |  |  | Can Publish Passport Product |
| POST | `/api/admin/passport-products/{product_id}/documents` | staff JWT + menu | PassportProductDocumentIn |  | Add Passport Document |
| POST | `/api/admin/passport-products/{product_id}/documents/reorder` | staff JWT + menu | array[object] |  | Reorder Passport Documents |
| DELETE | `/api/admin/passport-products/{product_id}/documents/{doc_id}` | staff JWT + menu |  |  | Delete Passport Document |
| PATCH | `/api/admin/passport-products/{product_id}/documents/{doc_id}` | staff JWT + menu | PassportProductDocumentIn |  | Patch Passport Document |
| POST | `/api/admin/passport-products/{product_id}/fees` | staff JWT + menu | PassportProductFeesIn |  | Set Passport Fees |
| POST | `/api/admin/passport-products/{product_id}/fields` | staff JWT + menu | PassportProductFieldIn |  | Add Passport Field |
| POST | `/api/admin/passport-products/{product_id}/fields/reorder` | staff JWT + menu | array[object] |  | Reorder Passport Fields |
| DELETE | `/api/admin/passport-products/{product_id}/fields/{field_id}` | staff JWT + menu |  |  | Delete Passport Field |
| PATCH | `/api/admin/passport-products/{product_id}/publish` | staff JWT + menu |  |  | Publish Passport Product |
| PATCH | `/api/admin/passport-products/{product_id}/unpublish` | staff JWT + menu |  |  | Unpublish Passport Product |
| GET | `/api/passport-products` | staff JWT |  | q, limit, offset, id | List Public Passport Products |

## roles

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/admin/roles` | staff JWT + menu |  | active | List Roles |
| POST | `/api/admin/roles` | staff JWT + menu | RoleCreateIn |  | Create Role |
| GET | `/api/admin/roles/catalog` | staff JWT + menu |  |  | Role Catalog |
| DELETE | `/api/admin/roles/{role_id}` | staff JWT + menu |  |  | Delete Role |
| PATCH | `/api/admin/roles/{role_id}` | staff JWT + menu | RoleUpdateIn |  | Update Role |

## visa_products

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/admin/visa-products` | staff JWT + menu |  | q, limit, offset, id | List All Products |
| POST | `/api/admin/visa-products` | staff JWT + menu | VisaProductIn |  | Create Product |
| POST | `/api/admin/visa-products/reorder` | staff JWT + menu | array[ReorderItemIn] |  | Reorder Products |
| GET | `/api/admin/visa-products/{product_id}` | staff JWT + menu |  |  | Get Admin Product |
| PATCH | `/api/admin/visa-products/{product_id}` | staff JWT + menu | VisaProductIn |  | Update Product |
| GET | `/api/admin/visa-products/{product_id}/can-publish` | staff JWT + menu |  |  | Check Publish |
| POST | `/api/admin/visa-products/{product_id}/documents` | staff JWT + menu | VisaProductDocumentIn |  | Add Document |
| POST | `/api/admin/visa-products/{product_id}/documents/reorder` | staff JWT + menu | array[object] |  | Reorder Documents |
| DELETE | `/api/admin/visa-products/{product_id}/documents/{doc_id}` | staff JWT + menu |  |  | Delete Document |
| PATCH | `/api/admin/visa-products/{product_id}/documents/{doc_id}` | staff JWT + menu | VisaProductDocumentIn |  | Patch Document |
| POST | `/api/admin/visa-products/{product_id}/fees` | staff JWT + menu | VisaProductFeesIn |  | Set Fees |
| POST | `/api/admin/visa-products/{product_id}/fields` | staff JWT + menu | VisaProductFieldIn |  | Add Field |
| POST | `/api/admin/visa-products/{product_id}/fields/reorder` | staff JWT + menu | array[object] |  | Reorder Fields |
| DELETE | `/api/admin/visa-products/{product_id}/fields/{field_id}` | staff JWT + menu |  |  | Delete Field |
| PATCH | `/api/admin/visa-products/{product_id}/publish` | staff JWT + menu |  |  | Publish Product |
| PATCH | `/api/admin/visa-products/{product_id}/unpublish` | staff JWT + menu |  |  | Unpublish Product |

## auth

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| POST | `/api/auth/staff/2fa/disable` | staff JWT | TwoFactorCodeIn |  | Staff 2Fa Disable |
| POST | `/api/auth/staff/2fa/enable` | staff JWT | TwoFactorCodeIn |  | Staff 2Fa Enable |
| POST | `/api/auth/staff/2fa/generate` | staff JWT | TwoFactorGenerateIn |  | Staff 2Fa Generate |
| POST | `/api/auth/staff/login` | public | LoginIn |  | Staff Login |
| POST | `/api/auth/staff/verify-2fa` | public | Verify2FAIn |  | Staff Verify 2Fa |

## documents

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| POST | `/api/documents/staff-upload` | staff JWT | multipart/form-data (`file`) |  | Staff Upload |

## media

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| POST | `/api/media/product-banner` | staff JWT | multipart/form-data (`file`) |  | Upload Product Banner |

## staff_me

| Method | Path | Auth | Body | Query | Summary |
|---|---|---|---|---|---|
| GET | `/api/staff/me` | staff JWT |  |  | Me |
| PATCH | `/api/staff/me` | staff JWT | StaffProfileIn |  | Update Me |
| POST | `/api/staff/me/change-password` | staff JWT | ChangePasswordIn |  | Change Password |

## Menu keys (CRM / admin)

- `/api/admin/consultants*`: `user_master`
- `/api/admin/roles*`: `role_master` (list also allowed with `user_master`)
- `/api/admin/visa-products*`: `visa_products`
- `/api/admin/passport-products*`: `passport_products`
- `/api/admin/document-master*`: `document_master`
- `/api/admin/field-master*`: `field_master`
- `/api/admin/settings*`: `case_numbers` or `visa_products`
