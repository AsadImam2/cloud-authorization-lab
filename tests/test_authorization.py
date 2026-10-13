from policies import authorize


def test_viewer_can_read_records():
    assert authorize("viewer", "record", "read") is True


def test_viewer_cannot_delete_records():
    assert authorize("viewer", "record", "delete") is False


def test_support_can_update_records():
    assert authorize("support", "record", "update") is True


def test_support_cannot_delete_records():
    assert authorize("support", "record", "delete") is False


def test_admin_can_delete_records():
    assert authorize("admin", "record", "delete") is True


def test_unknown_role_is_denied():
    assert authorize("guest", "record", "read") is False


def test_unknown_action_is_denied():
    assert authorize("admin", "record", "export") is False


def test_viewer_cannot_read_confidential_record():
    context = {"classification": "confidential"}

    assert authorize(
        "viewer", "record", "read", context
    ) is False


def test_support_cannot_read_confidential_record():
    context = {"classification": "confidential"}

    assert authorize(
        "support", "record", "read", context
    ) is False


def test_admin_can_read_confidential_record():
    context = {"classification": "confidential"}

    assert authorize(
        "admin", "record", "read", context
    ) is True

def test_default_classification_is_internal():
    assert authorize("viewer", "record", "read") is True


def test_unknown_classification_is_denied():
    context = {"classification": "top-secret"}

    assert authorize(
        "support", "record", "read", context
    ) is False

def test_admin_can_delete_confidential_record():
    context = {"classification": "confidential"}

    assert authorize(
        "admin", "record", "delete", context
    ) is True