import json

import pytest

from zendesk_toolkit.help_center import translations


@pytest.mark.parametrize("parent", ["articles", "sections", "categories"])
def test_create_translation_builds_url_for_each_parent(parent, client, base_url, mocked):
    mocked.add(
        mocked.POST,
        f"{base_url}/help_center/{parent}/9/translations.json",
        json={"translation": {}},
        status=201,
    )
    translations.create_translation(
        client, parent=parent, parent_id=9, translation={"locale": "fr", "title": "x", "body": "y"}
    )
    body = json.loads(mocked.calls[0].request.body)
    assert body == {"translation": {"locale": "fr", "title": "x", "body": "y"}}


def test_invalid_parent_rejected(client):
    with pytest.raises(ValueError):
        translations.list_translations(client, parent="posts", parent_id=1)


def test_delete_translation_uses_flat_endpoint(client, base_url, mocked):
    mocked.add(mocked.DELETE, f"{base_url}/help_center/translations/77.json", body="", status=204)
    assert translations.delete_translation(client, translation_id=77) is None
