# Contributing

Thanks for wanting to extend the toolkit. The library is small and opinionated; this guide focuses on the conventions that aren't obvious from the file tree.

## Dev setup

This repo uses [`uv`](https://docs.astral.sh/uv/) for environment and dependency management. The build backend is hatchling.

```bash
uv sync                   # creates .venv, installs runtime + dev dependencies (PEP 735 [dependency-groups] dev)
uv run pre-commit install # wires up the git hooks (runs ruff, mypy, pytest, etc. on commit)
```

Quick commands:

```bash
uv run pytest -q                                       # full suite (currently 36 tests, <1s)
uv run ruff check . && uv run ruff format --check .    # lint + format
uv run mypy                                            # type-check (scoped to zendesk_toolkit/ via pyproject)
uv run pre-commit run --all-files                      # everything at once
```

Python `>=3.11`. Adding a dep: `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (dev tooling).

## Project layout

See `CLAUDE.md` for the full architecture overview. The short version:

```
zendesk_toolkit/
  client.py         # ZendeskClient, JsonDict, ParamsType — shared
  errors.py         # ZendeskError
  pagination.py     # paginate_offset / paginate_cursor
  support/          # Zendesk Support API resources
  help_center/      # Zendesk Help Center (Guide) API resources
```

Both namespaces share **one** `ZendeskClient`. Don't add a second client.

## Adding a new endpoint

The vast majority of contributions look like this. Pick the right namespace (`support/` or `help_center/`) and the right module, then add a free function:

```python
def get_thing(client: ZendeskClient, thing_id: int) -> Optional[JsonDict]:
    return client.get(f"things/{thing_id}.json")
```

Conventions, in priority order:

1. **Free functions only.** First argument is always `client: ZendeskClient`. No classes, no state.
2. **Return type is `Optional[JsonDict]`.** The client returns `None` for empty 2xx bodies (e.g. 204 DELETE). Don't lie to callers.
3. **Wrap envelopes inside the function.** Callers pass the inner object; the function adds `{"ticket": ...}` / `{"article": ...}` / `{"translation": ...}` etc. before posting.
4. **Help Center locale scoping**: for endpoints that have `/api/v2/help_center/...` and `/api/v2/help_center/{locale}/...` variants, take an optional `locale: Optional[str] = None` kwarg and use the `_scope(locale)` helper at the top of the module. Don't duplicate the function.
5. **Multipart uploads**: pass `files=` to `client.post`. The client suppresses the JSON `Content-Type` automatically so `requests` can set the multipart boundary. Don't override `Content-Type` yourself.
6. **Update `REFERENCE.md`** in the same PR — the function reference is the user-facing index and goes stale fast otherwise.

### When to add a new module vs. extend an existing one

Add a new module when the resource has its own URL prefix and a coherent set of operations (e.g. `votes.py`, `labels.py`). Otherwise extend the closest existing module. Register the new module in the namespace's `__init__.py`.

## Tests

`tests/` uses `pytest` and the `responses` library to mock the requests HTTP layer. There are two gotchas worth flagging up front:

- **Use the `client` fixture** from `tests/conftest.py`, not a hand-rolled `ZendeskClient()`. It's constructed with `max_retries=0` so the urllib3 Retry adapter doesn't intercept 429/5xx — tests need to see those statuses to verify error wrapping and the explicit 429 backoff loop.
- **Mock with `responses` queues**, not absolute counts. `mocked.add(...)` appends one response; consecutive requests to the same URL pop them in order.

Minimal test template:

```python
def test_my_thing(client, base_url, mocked):
    mocked.add(mocked.GET, f"{base_url}/things/1.json", json={"thing": {"id": 1}}, status=200)
    result = my_module.get_thing(client, thing_id=1)
    assert result == {"thing": {"id": 1}}
    assert mocked.calls[0].request.url.endswith("/things/1.json")
```

For every new function, add at least:
- A happy-path test that pins the URL and the request body (for POST/PUT).
- An edge case if there's branching logic (locale scoping, optional filters, parent validation, etc.).

## Style / quality gates

`ruff` and `mypy` run on every commit via pre-commit. The configured rule sets are `E,F,I,UP,B,SIM`. Notes on what tends to surprise people:

- `UP006`/`UP035` mean `list[int]` / `dict[str, Any]` over `typing.List` / `typing.Dict`. `Optional[X]` is the in-tree convention even though `X | None` is valid on 3.11+ — `UP007`/`UP045` are explicitly ignored in `pyproject.toml` to keep the codebase consistent. If you want to flip and modernize, do it as its own PR.
- Don't add docstrings explaining what the code obviously does. Add one only when the *why* is non-obvious (a hidden Zendesk API quirk, a workaround, an invariant the reader can't infer).
- Don't add backwards-compatibility shims, dead-code re-exports, or "this used to be called X" comments. Pre-1.0; rename freely.

## Pull requests

- Keep the PR scoped. One namespace expansion (e.g. "add Help Center community/posts") is the right unit — not "add 4 unrelated endpoints across both APIs."
- The PR should leave the suite green: `uv run pytest -q`, `uv run ruff check`, `uv run ruff format --check`, `uv run mypy` all clean. Pre-commit enforces this locally.
- Include a test plan in the description listing the endpoints touched and how you verified them (the test cases, plus a one-line note if you also tested against a real Zendesk subdomain).
- Update `REFERENCE.md` and, when adding a new namespace or significant capability, `README.md`.
