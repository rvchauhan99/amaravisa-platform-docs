#!/usr/bin/env python3
"""Build dummy request/response examples for every OpenAPI operation."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "openapi" / "openapi.json").read_text())
SCHEMAS = SPEC.get("components", {}).get("schemas", {})

DUMMY_ID = "11111111-1111-4111-8111-111111111111"
DUMMY_ID_2 = "22222222-2222-4222-8222-222222222222"
DUMMY_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy"
NOW = "2026-09-08T10:00:00+00:00"

STAFF_USER = {
    "id": DUMMY_ID,
    "email": "staff@example.com",
    "full_name": "Priya Shah",
    "role": "consultant",
    "role_name": "Consultant",
    "menu_keys": [
        "dashboard",
        "pipeline",
        "tasks",
        "leads",
        "clients",
        "follow_ups",
    ],
    "unrestricted_scope": False,
    "country_codes": ["USA"],
    "two_factor_enabled": False,
}

ADMIN_USER = {
    **STAFF_USER,
    "email": "admin@visaconsult.demo",
    "full_name": "Ananya Rao (Admin)",
    "role": "admin",
    "role_name": "Admin",
    "menu_keys": ["dashboard", "pipeline", "user_master", "role_master"],
    "unrestricted_scope": True,
    "country_codes": [],
}

CUSTOMER_USER = {
    "id": DUMMY_ID,
    "email": "priya@example.com",
    "full_name": "Priya Shah",
}

CASE_ITEM = {
    "id": DUMMY_ID,
    "case_number": "AV-2026-0001",
    "stage": "docs_pending",
    "payment_status": "paid",
    "country_code": "USA",
    "assigned_consultant_id": DUMMY_ID_2,
    "customer_id": DUMMY_ID,
    "created_at": NOW,
}


def classify(path: str) -> str:
    if path.startswith("/api/crm"):
        return "crm"
    if (
        path.startswith("/api/admin")
        or path.startswith("/api/staff")
        or path.startswith("/api/auth/staff")
        or path.startswith("/api/media")
        or path.startswith("/api/passport-products")
        or path == "/api/documents/staff-upload"
    ):
        return "admin"
    return "customer"


def auth_note(path: str, tag: str) -> str:
    if path in {"/api/", "/api/health"}:
        return "public"
    if path.startswith("/api/visa-products") and "/admin/" not in path:
        return "public"
    if path == "/api/cases/webhooks/razorpay":
        return "webhook HMAC"
    if path == "/api/documents/download":
        return "signed token query"
    if path.startswith("/api/auth/customer"):
        return "public"
    if path.startswith("/api/auth/staff/login") or path.startswith("/api/auth/staff/verify-2fa"):
        return "public"
    if tag == "crm":
        return "staff JWT"
    if tag == "admin":
        if path.startswith("/api/staff") or path == "/api/documents/staff-upload" or path.startswith("/api/media"):
            return "staff JWT"
        if path.startswith("/api/auth/staff"):
            return "staff JWT"
        if path.startswith("/api/passport-products") and "/admin/" not in path:
            return "staff JWT"
        return "staff JWT + menu"
    return "customer JWT"


def resolve(schema: dict | None, depth: int = 0) -> dict:
    if not schema or depth > 8:
        return {}
    if "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        return resolve(SCHEMAS.get(name) or {}, depth + 1)
    if "allOf" in schema:
        merged: dict = {}
        for part in schema["allOf"]:
            merged.update(resolve(part, depth + 1))
        return merged or schema
    if "anyOf" in schema or "oneOf" in schema:
        options = schema.get("anyOf") or schema.get("oneOf") or []
        for opt in options:
            if opt.get("type") != "null" and "$ref" in opt or opt.get("type"):
                return resolve(opt, depth + 1)
        return resolve(options[0], depth + 1) if options else {}
    return schema


def fake_string(name: str, schema: dict) -> str:
    fmt = schema.get("format") or ""
    enum = schema.get("enum")
    if enum:
        return enum[0]
    key = (name or "").lower()
    if fmt == "email" or "email" in key:
        return "priya@example.com"
    if fmt == "date" or key.endswith("_date") or key in {"dob", "check_in", "check_out"}:
        return "2026-09-08"
    if fmt in {"date-time", "datetime"} or key.endswith("_at"):
        return NOW
    if "password" in key:
        return "Test@123"
    if key in {"id", "cid", "case_id", "lead_id", "customer_id", "consultant_id", "product_id", "draft_id", "role_id", "order_id", "invoice_id", "task_id", "doc_id", "field_id", "review_id", "appointment_id", "quotation_id", "profile_id", "vault_id", "master_id"} or key.endswith("_id"):
        return DUMMY_ID
    if "phone" in key:
        return "+919876543210"
    if "country" in key:
        return "USA"
    if key in {"currency"}:
        return "INR"
    if "url" in key:
        return "https://example.com/file.pdf"
    if key in {"code"}:
        return "123456"
    if "token" in key:
        return DUMMY_JWT
    if key in {"role", "slug"}:
        return "consultant"
    if key in {"stage", "target_stage"}:
        return "docs_pending"
    if key in {"status"}:
        return "new"
    if key in {"channel"}:
        return "phone"
    if key in {"outcome"}:
        return "interested"
    if key in {"full_name", "name", "default_name", "default_label", "title", "label"}:
        return "Sample Name"
    if key in {"body", "notes", "description", "reason"}:
        return "Sample note for integration testing."
    return f"sample_{name or 'value'}"


def fake_from_schema(schema: dict | None, name: str = "", depth: int = 0):
    schema = resolve(schema, depth)
    if not schema:
        return None
    if schema.get("enum"):
        return schema["enum"][0]
    typ = schema.get("type")
    if typ == "array" or "items" in schema:
        item = fake_from_schema(schema.get("items") or {"type": "string"}, name, depth + 1)
        return [item]
    if typ == "object" or schema.get("properties"):
        out = {}
        props = schema.get("properties") or {}
        required = set(schema.get("required") or [])
        keys = list(props) if not required else [k for k in props if k in required] + [k for k in props if k not in required]
        for key in keys[:24]:
            out[key] = fake_from_schema(props[key], key, depth + 1)
        if schema.get("additionalProperties") and not out:
            out["key"] = "value"
        return out
    if typ == "integer":
        return 1
    if typ == "number":
        return 100.0
    if typ == "boolean":
        return True
    if typ == "null":
        return None
    return fake_string(name, schema)


def paged(items: list, extra_summary: dict | None = None) -> dict:
    out = {
        "items": items,
        "meta": {
            "page": 1,
            "limit": 25,
            "total": len(items),
            "pages": 1,
            "has_more": False,
        },
    }
    if extra_summary is not None:
        out["summary"] = extra_summary
    return out


BODY_OVERRIDES = {
    "LoginIn": {"email": "priya@example.com", "password": "Test@123"},
    "CustomerRegisterIn": {
        "email": "priya@example.com",
        "password": "Test@123",
        "full_name": "Priya Shah",
        "phone": "+919876543210",
    },
    "CustomerVerifyOtpIn": {"pending_token": DUMMY_JWT, "code": "123456"},
    "CustomerResendOtpIn": {"pending_token": DUMMY_JWT},
    "CustomerGoogleIn": {"id_token": "ya29.dummy-google-id-token", "mode": "login"},
    "CustomerForgotPasswordIn": {"email": "priya@example.com"},
    "CustomerForgotPasswordResetIn": {
        "email": "priya@example.com",
        "code": "123456",
        "new_password": "NewPass@123",
    },
    "Verify2FAIn": {"temp_token": DUMMY_JWT, "code": "123456"},
    "TwoFactorCodeIn": {"code": "123456"},
    "TwoFactorGenerateIn": {"issuer": "AmaraVisa CRM"},
    "ChangePasswordIn": {
        "current_password": "Test@123",
        "new_password": "NewPass@123",
        "confirm_password": "NewPass@123",
    },
    "StaffCreateIn": {
        "email": "new.staff@example.com",
        "password": "Test@123",
        "full_name": "New Staff",
        "role": "consultant",
        "country_codes": ["USA"],
        "manager_id": None,
    },
    "StaffUpdateIn": {
        "email": "staff@example.com",
        "full_name": "Priya Shah",
        "role": "consultant",
        "country_codes": ["USA"],
        "manager_id": None,
        "password": None,
    },
    "RoleCreateIn": {
        "name": "Operations lead",
        "slug": "operations-lead",
        "menu_keys": ["pipeline", "tasks"],
    },
    "RoleUpdateIn": {"name": "Operations lead", "menu_keys": ["pipeline", "tasks"], "active": True},
    "CaseDraftIn": {
        "visa_product_id": DUMMY_ID,
        "traveler": {"full_name": "Priya Shah", "passport_number": "P1234567"},
        "field_values": {"travel_date": "2026-10-01"},
        "document_uploads": [{"doc_key": "passport", "file_url": "https://example.com/p.pdf", "filename": "passport.pdf"}],
    },
    "MockCheckoutIn": {"draft_id": DUMMY_ID, "outcome": "success"},
    "PaymentConfirmIn": {
        "draft_id": DUMMY_ID,
        "order_id": "order_demo_1",
        "payment_id": "pay_demo_1",
        "signature": "dummy_signature",
        "outcome": "success",
    },
    "LeadIn": {
        "full_name": "Rahul Patel",
        "email": "rahul@example.com",
        "phone": "+919811122233",
        "country_code": "USA",
        "source": "website",
        "status": "new",
        "service_type": "visa",
        "service_details": {"adults": 1, "children": 0, "country_code": "USA", "visa_type": "tourist"},
        "lead_value": 15000.0,
    },
    "LeadBatchCreateIn": {
        "full_name": "Rahul Patel",
        "email": "rahul@example.com",
        "phone": "+919811122233",
        "status": "new",
        "services": [
            {"service_type": "visa", "service_details": {"country_code": "USA", "adults": 1}},
            {"service_type": "hotel_booking", "service_details": {"destination": "New York", "rooms": 1}},
        ],
    },
    "LeadConvertIn": {
        "visa_product_id": DUMMY_ID,
        "traveler": {"full_name": "Rahul Patel"},
        "create_case": True,
        "create_order": True,
    },
    "LeadFollowUpIn": {
        "channel": "phone",
        "outcome": "follow_up",
        "notes": "Called, will decide next week.",
        "next_follow_up_at": "2026-09-15T10:00:00+00:00",
    },
    "OfflineCaseIn": {
        "visa_product_id": DUMMY_ID,
        "customer_email": "rahul@example.com",
        "customer_full_name": "Rahul Patel",
        "customer_phone": "+919811122233",
        "traveler": {"full_name": "Rahul Patel"},
        "field_values": {},
        "document_uploads": [],
        "payment_status": "pending",
    },
    "VisaProductIn": {
        "country_code": "USA",
        "country_name": "United States",
        "visa_type": "tourist",
        "visa_format": "e_visa",
        "title": "USA Tourist Visa",
        "validity_days": 180,
        "processing_time_days": 21,
        "passport_min_validity_months": 6,
    },
    "PassportProductIn": {
        "title": "Passport reissue",
        "passport_service_type": "reissue",
        "processing_time_days": 7,
    },
    "InvoiceIn": {
        "case_id": DUMMY_ID,
        "customer_id": DUMMY_ID_2,
        "amount": 18500.0,
        "currency": "INR",
        "due_date": "2026-09-20",
        "line_items": [{"label": "Service fee", "amount": 18500.0}],
    },
    "PaymentLedgerIn": {
        "amount": 18500.0,
        "payment_type": "payment",
        "method": "upi",
        "reference": "UPI123",
    },
}

RESPONSE_OVERRIDES = {
    ("get", "/api/"): {"service": "Visa Consultancy API", "status": "ok"},
    ("get", "/api/health"): {"status": "ok"},
    ("post", "/api/auth/customer/register"): {"pending_token": DUMMY_JWT, "email": "priya@example.com"},
    ("post", "/api/auth/customer/register/resend-otp"): {"ok": True, "email": "priya@example.com"},
    ("post", "/api/auth/customer/register/verify-otp"): {
        "access_token": DUMMY_JWT,
        "token_type": "bearer",
        "user": CUSTOMER_USER,
    },
    ("post", "/api/auth/customer/login"): {
        "access_token": DUMMY_JWT,
        "token_type": "bearer",
        "user": CUSTOMER_USER,
    },
    ("post", "/api/auth/customer/google"): {
        "access_token": DUMMY_JWT,
        "token_type": "bearer",
        "user": CUSTOMER_USER,
        "is_new_user": False,
    },
    ("post", "/api/auth/customer/forgot-password"): {
        "detail": "If an account exists, a reset code has been sent."
    },
    ("post", "/api/auth/customer/forgot-password/reset"): {"ok": True},
    ("post", "/api/auth/staff/login"): {
        "access_token": DUMMY_JWT,
        "token_type": "bearer",
        "user": ADMIN_USER,
    },
    ("post", "/api/auth/staff/verify-2fa"): {
        "access_token": DUMMY_JWT,
        "token_type": "bearer",
        "user": ADMIN_USER,
    },
    ("post", "/api/auth/staff/2fa/generate"): {
        "secret": "JBSWY3DPEHPK3PXP",
        "otpauth_uri": "otpauth://totp/AmaraVisa:staff@example.com?secret=JBSWY3DPEHPK3PXP",
        "qr_data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB",
    },
    ("post", "/api/auth/staff/2fa/enable"): {"ok": True, "two_factor_enabled": True},
    ("post", "/api/auth/staff/2fa/disable"): {"ok": True, "two_factor_enabled": False},
    ("get", "/api/staff/me"): {**STAFF_USER, "country_codes": ["USA"]},
    ("post", "/api/cases"): {"draft_id": DUMMY_ID},
    ("post", "/api/cases/checkout/create-order"): {
        "mode": "mock",
        "order_id": "order_demo_1",
        "key_id": None,
        "amount": 1850000,
        "currency": "INR",
    },
    ("post", "/api/cases/checkout"): {"case_id": DUMMY_ID, "case_number": "AV-2026-0001"},
    ("post", "/api/documents/upload"): {
        "file_url": "https://example.com/signed/passport.pdf",
        "filename": "passport.pdf",
        "doc_key": "passport",
    },
    ("post", "/api/documents/staff-upload"): {
        "file_url": "https://example.com/signed/passport.pdf",
        "filename": "passport.pdf",
    },
    ("post", "/api/documents/scan-passport"): {
        "full_name": "RAHUL KUMAR PATEL",
        "passport_number": "P1234567",
        "date_of_birth": "1995-01-01",
        "passport_issue_date": "2025-01-01",
        "passport_expiry_date": "2035-01-01",
        "gender": "Male",
        "nationality": "IND",
        "ocr_confidence": 0.97,
        "request_id": "ocr_demo_1",
        "warnings": [],
    },
    ("get", "/api/documents/download"): "<binary file stream>",
    ("post", "/api/media/product-banner"): {
        "url": "https://cdn.example.com/banners/usa.webp"
    },
    ("get", "/api/visa-products/countries"): {
        "items": [
            {"code": "USA", "name": "United States", "flag": "🇺🇸"},
            {"code": "IND", "name": "India", "flag": "🇮🇳"},
            {"code": "SCH", "name": "Schengen (Europe)", "flag": "🇪🇺"},
        ],
        "total": 250,
        "has_more": True,
    },
    ("post", "/api/cases/webhooks/razorpay"): {"ok": True},
    ("get", "/api/crm/cases"): paged([CASE_ITEM]),
    ("get", "/api/crm/cases/{case_id}"): {
        **CASE_ITEM,
        "traveler": {"full_name": "Priya Shah", "passport_number": "P1234567"},
        "documents": [{"id": DUMMY_ID, "doc_key": "passport", "status": "received"}],
    },
    ("get", "/api/admin/roles"): [
        {
            "id": DUMMY_ID,
            "slug": "admin",
            "name": "Admin",
            "menu_keys": ["dashboard", "role_master", "user_master"],
            "unrestricted_scope": True,
            "is_system": True,
            "active": True,
        }
    ],
    ("get", "/api/admin/roles/catalog"): [
        {"key": "dashboard", "label": "Dashboard", "group": "Insights", "group_id": "insights"},
        {"key": "pipeline", "label": "Pipeline", "group": "Cases", "group_id": "cases"},
        {"key": "role_master", "label": "Role Master", "group": "Admin", "group_id": "admin"},
    ],
    ("post", "/api/admin/roles"): {
        "id": DUMMY_ID,
        "slug": "operations-lead",
        "name": "Operations lead",
        "menu_keys": ["pipeline", "tasks"],
        "unrestricted_scope": False,
        "is_system": False,
        "active": True,
    },
    ("post", "/api/admin/consultants"): {"id": DUMMY_ID, "country_codes": ["USA"]},
    ("get", "/api/crm/reports/dashboard"): {
        "open_cases": 12,
        "overdue": 2,
        "revenue": 185000,
        "leads_new": 8,
        "service_lanes": ["visa", "passport"],
    },
}


def schema_name(schema: dict | None) -> str:
    if not schema:
        return ""
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]
    if schema.get("type") == "array":
        return schema_name(schema.get("items") or {})
    return schema.get("title") or ""


def request_example(op: dict, path: str) -> tuple[dict | None, str | None]:
    body = op.get("requestBody") or {}
    content = body.get("content") or {}
    if "multipart/form-data" in content:
        return (
            {"file": "<binary>", "_note": "Send as multipart/form-data field named file"},
            "multipart/form-data",
        )
    if path == "/api/cases/webhooks/razorpay":
        return (
            {
                "event": "payment.captured",
                "payload": {"payment": {"entity": {"id": "pay_demo_1", "order_id": "order_demo_1"}}},
            },
            "application/json",
        )
    path_bodies = {
        "/api/auth/staff/login": {"email": "admin@visaconsult.demo", "password": "Admin@123"},
        "/api/auth/customer/login": {"email": "priya@example.com", "password": "Test@123"},
    }
    if path in path_bodies:
        return deepcopy(path_bodies[path]), "application/json"
    json_body = content.get("application/json")
    if not json_body:
        return None, None
    schema = json_body.get("schema") or {}
    name = schema_name(schema)
    if name in BODY_OVERRIDES:
        return deepcopy(BODY_OVERRIDES[name]), "application/json"
    if schema.get("type") == "array" or (isinstance(schema.get("items"), dict)):
        inner = schema.get("items") or {}
        inner_name = schema_name(inner)
        if inner_name == "ReorderItemIn" or "reorder" in path:
            return [{"id": DUMMY_ID, "display_order": 1}], "application/json"
        if "string" in str(inner.get("type")) or inner_name == "":
            if "countries" in path:
                return ["USA", "GBR"], "application/json"
        return [fake_from_schema(inner, "item")], "application/json"
    return fake_from_schema(schema, name), "application/json"


def path_params(path: str) -> dict:
    names = re.findall(r"\{([^}]+)\}", path)
    return {n: DUMMY_ID for n in names}


def query_example(op: dict) -> dict:
    out = {}
    for p in op.get("parameters") or []:
        if p.get("in") != "query":
            continue
        name = p.get("name") or "q"
        schema = p.get("schema") or {}
        if name in {"page"}:
            out[name] = 1
        elif name in {"limit", "offset"}:
            out[name] = 25 if name == "limit" else 0
        elif name in {"q"}:
            out[name] = "usa"
        elif schema.get("type") == "boolean":
            out[name] = False
        elif schema.get("type") in {"integer", "number"}:
            out[name] = 1
        else:
            out[name] = fake_string(name, schema)
    return out


def headers_for(path: str, tag: str, content_type: str | None) -> dict:
    headers = {}
    if content_type:
        headers["Content-Type"] = content_type
    auth = auth_note(path, tag)
    if "staff JWT" in auth:
        headers["Authorization"] = f"Bearer {DUMMY_JWT}"
    elif auth == "customer JWT":
        headers["Authorization"] = f"Bearer {DUMMY_JWT}"
    elif auth == "webhook HMAC":
        headers["X-Razorpay-Signature"] = "dummy_hmac_signature"
    if path == "/api/documents/download":
        # token is query; no bearer required
        headers.pop("Authorization", None)
    return headers


def looks_like_list(method: str, path: str, op: dict) -> bool:
    if method != "get":
        return False
    names = {p.get("name") for p in (op.get("parameters") or []) if p.get("in") == "query"}
    if {"page", "limit"} & names:
        return True
    if re.search(r"\{[^}]+\}$", path):
        return False
    return path.rstrip("/").split("/")[-1] in {
        "cases",
        "leads",
        "clients",
        "tasks",
        "invoices",
        "quotations",
        "appointments",
        "communications",
        "consultants",
        "roles",
        "visa-products",
        "passport-products",
        "service-orders",
        "payments",
        "drafts",
        "traveler-profiles",
        "document-vault",
        "document-master",
        "field-master",
        "qa-reviews",
        "countries",
        "notifications",
        "birthdays",
    }


def default_response(method: str, path: str, op: dict):
    key = (method, path)
    if key in RESPONSE_OVERRIDES:
        return deepcopy(RESPONSE_OVERRIDES[key])
    if method == "delete":
        return {"ok": True}
    if looks_like_list(method, path, op):
        item = {"id": DUMMY_ID, "name": "Sample", "created_at": NOW}
        if "visa-products" in path:
            item = {"id": DUMMY_ID, "title": "USA Tourist Visa", "country_code": "USA", "status": "published"}
        if path.endswith("/admin/consultants") or path.endswith("/crm/consultants"):
            item = {**STAFF_USER}
        return paged([item])
    if method == "patch" and path.endswith("/activate"):
        return {"ok": True, "active": True}
    if method == "patch" and path.endswith("/deactivate"):
        return {"ok": True, "active": False}
    if method in {"post", "patch"}:
        return {"ok": True, "id": DUMMY_ID, "updated_at": NOW}
    return {"id": DUMMY_ID, "status": "ok"}


def response_status(method: str, path: str) -> int:
    if method == "post" and path.endswith("/register"):
        return 200
    return 200


def build() -> dict:
    apis = []
    for path, methods in sorted(SPEC.get("paths", {}).items()):
        for method, op in methods.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            tag = classify(path)
            body, ctype = request_example(op, path)
            headers = headers_for(path, tag, ctype)
            q = query_example(op)
            if path == "/api/documents/download":
                q = {"token": DUMMY_JWT}
            if path == "/api/visa-products/countries":
                q = {"q": "ind", "limit": 10, "offset": 0, "id": "USA"}
            entry = {
                "id": f"{method.upper()} {path}",
                "surface": tag,
                "method": method.upper(),
                "path": path,
                "auth": auth_note(path, tag),
                "headers": headers,
                "path_params": path_params(path),
                "query": q,
                "request_body": body,
                "response_status": response_status(method, path),
                "response_body": default_response(method, path, op),
            }
            apis.append(entry)
    return {
        "title": "AmaraVisa API examples",
        "base_url": "http://127.0.0.1:8000",
        "generated_from": "openapi/openapi.json + route/model review",
        "note": "Illustrative success payloads for integration. Not a production HAR. Errors typically return {\"detail\": \"...\"}.",
        "auth": {
            "customer": "Authorization: Bearer <customer_jwt>",
            "staff": "Authorization: Bearer <staff_jwt>",
        },
        "count": len(apis),
        "apis": apis,
    }


def main() -> None:
    data = build()
    out = ROOT / "openapi" / "api-examples.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} ({data['count']} operations)")


if __name__ == "__main__":
    main()
