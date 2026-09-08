#!/usr/bin/env python3
"""Generate human-readable API catalogs from the OpenAPI snapshot."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "openapi" / "openapi.json").read_text())
SCHEMAS = SPEC.get("components", {}).get("schemas", {})


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


def schema_name(ref_or_schema: dict | None) -> str:
    if not ref_or_schema:
        return ""
    if "$ref" in ref_or_schema:
        return ref_or_schema["$ref"].split("/")[-1]
    if ref_or_schema.get("type") == "array":
        inner = schema_name(ref_or_schema.get("items") or {})
        return f"array[{inner}]" if inner else "array"
    return ref_or_schema.get("type") or ""


def request_body(op: dict) -> str:
    body = op.get("requestBody") or {}
    content = body.get("content") or {}
    if "multipart/form-data" in content:
        return "multipart/form-data (`file`)"
    json_body = content.get("application/json") or {}
    name = schema_name(json_body.get("schema") or {})
    return name or ("JSON" if content else "")


def query_params(op: dict) -> str:
    parts = []
    for p in op.get("parameters") or []:
        if p.get("in") == "query":
            parts.append(p.get("name", ""))
    return ", ".join(parts)


def auth_note(path: str, tag: str) -> str:
    if path in {"/api/", "/api/health"}:
        return "public"
    if path.startswith("/api/visa-products") and "/admin/" not in path:
        return "public"
    if path == "/api/cases/webhooks/razorpay":
        return "webhook HMAC"
    if path == "/api/documents/download":
        return "signed `token` query"
    if path.startswith("/api/auth/customer") or path.startswith("/api/auth/staff/login") or path.startswith("/api/auth/staff/verify-2fa"):
        return "public"
    if tag == "crm":
        return "staff JWT (+ menu where noted)"
    if tag == "admin":
        if path.startswith("/api/auth/staff"):
            return "staff JWT" if "login" not in path and "verify-2fa" not in path else "public"
        if path.startswith("/api/staff"):
            return "staff JWT"
        if path.startswith("/api/passport-products") and "/admin/" not in path:
            return "staff JWT"
        if path == "/api/documents/staff-upload" or path.startswith("/api/media"):
            return "staff JWT"
        return "staff JWT + menu"
    return "customer JWT"


INTRO = {
    "customer": """# API catalog — customer platform and public

These endpoints power the **customer site** (Next.js) and public catalog. Base URL is the API origin plus `/api`.

Interactive docs: [Swagger UI](http://127.0.0.1:8000/docs) · [ReDoc](http://127.0.0.1:8000/redoc) · snapshot in [`openapi/openapi.json`](openapi/openapi.json).

Auth column is from the live route guards (OpenAPI does not always mark security). Request body names match Pydantic models — field lists are in [07-payloads-and-models.md](07-payloads-and-models.md).
""",
    "crm": """# API catalog — CRM / DASH (`/api/crm`)

These endpoints power the **staff CRM**. All require a staff JWT (`Authorization: Bearer`). Several also require a Role Master menu key (see [03-authentication-and-rbac.md](03-authentication-and-rbac.md)).

Interactive docs: [Swagger UI](http://127.0.0.1:8000/docs) · snapshot in [`openapi/openapi.json`](openapi/openapi.json).
""",
    "admin": """# API catalog — admin, staff self-service, and catalog builders

User Master, Role Master, visa/passport product builders, case-number settings, staff 2FA, and `/staff/me`. Most require a staff JWT **and** a menu key.

Interactive docs: [Swagger UI](http://127.0.0.1:8000/docs) · snapshot in [`openapi/openapi.json`](openapi/openapi.json).
""",
}

MENU_NOTES = {
    "/api/crm/cases": "`pipeline` for list/detail; `offline_case` for POST create; `tasks` for task routes",
    "/api/crm/reports/dashboard": "`dashboard`",
    "/api/crm/reports/leads": "`lead_analytics`",
    "/api/crm/reports/payments": "`payment_reports`",
    "/api/crm/payments": "`payment_reports`",
    "/api/crm/birthdays": "`birthdays`",
    "/api/crm/passport-expiry": "`passport_expiry`",
    "/api/crm/clients": "`clients`",
    "/api/crm/service-orders": "`service_orders`",
    "/api/crm/reports/pipeline": "`case_reports`",
    "/api/admin/consultants": "`user_master`",
    "/api/admin/roles": "`role_master` (list also allowed with `user_master`)",
    "/api/admin/visa-products": "`visa_products`",
    "/api/admin/passport-products": "`passport_products`",
    "/api/admin/document-master": "`document_master`",
    "/api/admin/field-master": "`field_master`",
    "/api/admin/settings": "`case_numbers` or `visa_products`",
}


def write_catalog(tag: str, rows: list[tuple[str, str, dict]]) -> None:
    names = {
        "customer": "04-api-catalog-customer.md",
        "crm": "05-api-catalog-crm.md",
        "admin": "06-api-catalog-admin.md",
    }
    lines = [INTRO[tag], "", f"**{len(rows)} operations** in this catalog.", ""]
    grouped: dict[str, list] = defaultdict(list)
    for method, path, op in rows:
        tags = ",".join(op.get("tags") or ["other"])
        grouped[tags].append((method, path, op))
    for group, items in grouped.items():
        lines.append(f"## {group}")
        lines.append("")
        lines.append("| Method | Path | Auth | Body | Query | Summary |")
        lines.append("|---|---|---|---|---|---|")
        for method, path, op in items:
            summary = (op.get("summary") or op.get("operationId") or "").replace("|", "/")
            body = request_body(op).replace("|", "/")
            q = query_params(op).replace("|", "/")
            auth = auth_note(path, tag)
            lines.append(f"| {method.upper()} | `{path}` | {auth} | {body} | {q} | {summary} |")
        lines.append("")
    extra = []
    for prefix, note in MENU_NOTES.items():
        if any(p.startswith(prefix) for _, p, _ in rows):
            extra.append(f"- `{prefix}*`: {note}")
    if extra:
        lines.append("## Menu keys (CRM / admin)")
        lines.append("")
        lines.extend(extra)
        lines.append("")
        if tag == "crm":
            lines.append("Leads, follow-ups, finance, inbox, appointments, quotations, invoices, and communications currently use **staff JWT only** (country/hierarchy scope). The CRM sidebar still hides those pages unless the role has the matching menu key.")
            lines.append("")
    (ROOT / names[tag]).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    buckets = {"customer": [], "crm": [], "admin": []}
    for path, methods in sorted(SPEC.get("paths", {}).items()):
        tag = classify(path)
        for method, op in methods.items():
            if method.startswith("x-") or method == "parameters":
                continue
            buckets[tag].append((method, path, op))
    for tag, rows in buckets.items():
        rows.sort(key=lambda r: (r[1], r[0]))
        write_catalog(tag, rows)
        print(f"{tag}: {len(rows)} operations")


if __name__ == "__main__":
    main()
