
from flask import Flask, jsonify, request
from policies import authorize
from audit import log_access

app = Flask(__name__)

# Public demo tokens for this local learning lab only.
# Never use hardcoded demo tokens in a real application.
DEMO_USERS = {
    "viewer-demo-token": {
        "user_id": "user-001",
        "role": "viewer",
    },
    "support-demo-token": {
        "user_id": "user-002",
        "role": "support",
    },
    "admin-demo-token": {
        "user_id": "user-003",
        "role": "admin",
    },
}



RECORDS = {
    "1": {
        "id": "1",
        "title": "User 001 report",
        "owner_id": "user-001",
        "classification": "internal",
    },
    "2": {
        "id": "2",
        "title": "User 002 report",
        "owner_id": "user-002",
        "classification": "confidential",
    },
}


def get_current_user():
    """Resolve a demo bearer token to a server-side identity."""
    auth_header = request.headers.get("Authorization", "")
    scheme, separator, token = auth_header.partition(" ")

    if not separator or scheme.lower() != "bearer":
        return None

    return DEMO_USERS.get(token)


@app.route("/")
def home():
    return jsonify({
        "message": "Cloud Authorization Lab API",
        "status": "running",
    })
    


@app.route("/records/<record_id>", methods=["GET", "DELETE"])
def manage_record(record_id):
    user = get_current_user()
    resource = f"record:{record_id}"

    if user is None:
        log_access(
            "unknown", "unknown", request.method,
            resource, "DENY"
        )
        return jsonify({"error": "Unauthorized"}), 401

    role = user["role"]
    user_id = user["user_id"]
    action = "read" if request.method == "GET" else "delete"

    record = RECORDS.get(record_id)

    if record is None:
        log_access(user_id, role, action, resource, "NOT_FOUND")
        return jsonify({"error": "Record not found"}), 404

    context = {
        "classification": record["classification"],
    }

    # RBAC + ABAC authorization
    if not authorize(role, "record", action, context):
        log_access(user_id, role, action, resource, "DENY")
        return jsonify({"error": "Forbidden"}), 403

    # Resource-level authorization
    if record["owner_id"] != user_id and role != "admin":
        log_access(user_id, role, action, resource, "DENY")
        return jsonify({"error": "Forbidden"}), 403

    if action == "delete":
        del RECORDS[record_id]
        log_access(user_id, role, action, resource, "ALLOW")
        return jsonify({"message": "Record deleted"}), 200

    log_access(user_id, role, action, resource, "ALLOW")
    return jsonify(record), 200



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
