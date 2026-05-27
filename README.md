# Zendesk API Python Library

*A lightweight, retry-safe Python client for the Zendesk Support and Help Center APIs with broad endpoint coverage and clean helpers.*

## Features

- ✅ API token **or** OAuth bearer authentication
- ♻️ Automatic retries for 429/5xx with `Retry-After` backoff
- ⏱️ Timeouts and session reuse
- 🔁 **Offset** and **Cursor** pagination helpers
- 🧱 Two namespaces sharing one HTTP client:
  - `zendesk_toolkit.support` — `tickets`, `users`, `organizations`, `groups`, `macros`, `views`, `custom_fields`, `uploads`, `side_conversations`, `search`, `comments`
  - `zendesk_toolkit.help_center` — `articles`, `categories`, `sections`, `translations`, `attachments`, `comments`, `labels`, `votes`, `search`, `locales`, `user_segments`
- ⚠️ Unified error handling via `ZendeskError` (includes HTTP status and `X-Request-Id`)

---

## Install

```bash
# With uv (recommended)
uv add zendesk-toolkit

# Or with pip
pip install zendesk-toolkit
```

Requires Python `>=3.11`.

---

## Quick Start — Support

```python
from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.support import tickets

client = ZendeskClient(
    subdomain="yoursubdomain",
    email="agent@company.com",
    token="ZENDESK_API_TOKEN",
)

resp = tickets.create_ticket(client, {
    "subject": "Printer on Floor 3 is jammed",
    "comment": {"body": "Happens every morning around 9am."},
    "priority": "normal",
})
print("New ticket:", resp["ticket"]["id"])
```

## Quick Start — Help Center

```python
from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.help_center import articles, search

client = ZendeskClient(
    subdomain="yoursubdomain",
    email="agent@company.com",
    token="ZENDESK_API_TOKEN",
)

# Create an article in a section
created = articles.create_article(client, section_id=12345, article={
    "title": "Resetting your password",
    "body": "<p>Click the reset link.</p>",
    "locale": "en-us",
}, locale="en-us")

# Search the Help Center
results = search.search_articles(client, query="password reset", locale="en-us")
```
