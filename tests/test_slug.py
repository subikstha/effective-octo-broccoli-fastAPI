def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def test_slugify_lowercases_and_dashes_and_spaces():
    assert slugify("Release Tracker") == "release-tracker"


def test_slugify_strips_whitespace():
    assert slugify("  Release Tracker  ") == "release-tracker"
