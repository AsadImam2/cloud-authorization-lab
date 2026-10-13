from typing import Any


ROLE_PERMISSIONS = {
    "viewer": {("record", "read")},
    "support": {("record", "read"), ("record", "update")},
    "admin": {
        ("record", "read"),
        ("record", "update"),
        ("record", "delete"),
    },
}


def authorize(
    role: str,
    resource_type: str,
    action: str,
    context: dict[str, Any] | None = None,
) -> bool:
    """Check role permissions and resource attributes."""

    # RBAC check
    if role not in ROLE_PERMISSIONS:
        return False

    if (resource_type, action) not in ROLE_PERMISSIONS[role]:
        return False

    # ABAC check
    context = context or {}
    classification = context.get("classification", "internal")

    # Deny unknown classifications
    if classification not in {"internal", "confidential"}:
        return False

    # Confidential records are admin-only
    if classification == "confidential":
        return role == "admin"

    return True