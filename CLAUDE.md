# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Install & run

```bash
pip install -e .   # editable install; pulls `requests>=2.32.0`
```

Python `>=3.9` (per `pyproject.toml`). No tests, lint, or CI. Verify changes by importing the package and exercising calls against a live Zendesk subdomain.

## Architecture

One shared HTTP client + two parallel resource namespaces, each a flat module of free functions. See `REFERENCE.md` for the full function index.

```
zendesk_toolkit/
  client.py            # ZendeskClient (auth, retries, base URL) — shared
  errors.py            # ZendeskError — shared
  pagination.py        # paginate_offset / paginate_cursor — shared
  support/             # Zendesk Support API
    tickets, users, organizations, groups, custom_fields, macros, views,
    comments, side_conversations, search, uploads
  help_center/         # Zendesk Help Center (Guide) API
    articles, categories, sections, translations, attachments, comments,
    labels, votes, search, locales, user_segments
```

- **`client.py`** — `ZendeskClient` owns the `requests.Session`, auth, base URL (`https://{subdomain}.zendesk.com/api/v2`), timeouts, and retries. Two layers of retry protect against 429/5xx: a urllib3 `Retry` adapter (`backoff_factor=1`, `total=5`, respects `Retry-After`) **and** an explicit 429 loop in `_request` that sleeps `Retry-After` and re-issues the request. `_request` accepts either a relative endpoint or a full URL — pagination helpers rely on this when following `links.next`.
- **Resource modules** — each is a thin module of free functions whose first argument is a `ZendeskClient`. They contain no state; all HTTP goes through the client. When adding a new endpoint, follow this pattern rather than introducing classes.
- **Both namespaces share one `ZendeskClient`.** Don't add a Help-Center–specific client. The Help Center modules hit `help_center/...` paths under the same `/api/v2` base URL the Support modules use.
- **`errors.py`** — every non-2xx response is converted to `ZendeskError(message, status, request_id, payload)`. Don't catch and swallow; callers depend on `.status` / `.request_id` for diagnostics.
- **`pagination.py`** — `paginate_offset` and `paginate_cursor` are generators that yield whole page dicts (not individual records). Offset increments `page`; cursor follows `links.next` and strips `client.base_url` to reuse `_request`'s relative-path mode.

## Conventions

- Import is `from zendesk_toolkit import ZendeskClient` plus `from zendesk_toolkit.support import …` or `from zendesk_toolkit.help_center import …`. There are intentionally no top-level re-exports of the resource modules — namespace clashes (e.g. both packages have a `search` and a `comments` module) make that a bad idea.
- Resource module functions return the raw JSON dict from Zendesk (e.g. `{"ticket": {...}}`, `{"article": {...}}`), not unwrapped objects. Callers index into the response.
- POST/PUT bodies are always wrapped in their Zendesk envelope (`{"ticket": ...}`, `{"article": ...}`, `{"translation": ...}`, etc.) inside the function — callers pass the inner object.
- **Help Center locale handling**: most resource functions take an optional `locale=` kwarg. When provided, the URL becomes `/help_center/{locale}/<resource>/...` (the variant required for anonymous/end-user reads); when omitted, the agent-only `/help_center/<resource>/...` variant is used. A single `_scope(locale)` helper at the top of each module builds this prefix.
- **Translations span three parent types.** `help_center/translations.py` exposes one set of functions parameterized by `parent ∈ {"articles", "sections", "categories"}` rather than three duplicate modules. Validate the parent against the allowed set.
- `support.tickets.add_comment_with_uploads` is the canonical multi-update example: a single PUT can combine a comment, upload tokens, custom fields, and arbitrary ticket-level updates. Prefer one combined PUT over multiple sequential updates whenever possible — it's atomic on Zendesk's side and avoids extra rate-limit pressure.
- File uploads (`support.uploads.upload_file`, `help_center.attachments.create_article_attachment`) are multipart; the client strips `Content-Type: application/json` automatically when `files=` is passed.

## Help Center scope

The current Help Center coverage is the core knowledge-base surface: articles, categories, sections, translations, article attachments/comments/labels, votes, search, locales, user segments. **Not yet wired up:** community (posts, topics, post comments), subscriptions, user images, service catalog, sessions, deflection/generative endpoints. These can be added as new modules under `help_center/` following the same free-function pattern when needed.
