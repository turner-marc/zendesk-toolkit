"""Create a Help Center article, add a translation, and search for it."""

from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.help_center import articles, search, translations

SUBDOMAIN = "your_subdomain"
EMAIL = "you@company.com"
API_TOKEN = "your_api_token"

SECTION_ID = 12345
LOCALE = "en-us"

client = ZendeskClient(subdomain=SUBDOMAIN, email=EMAIL, token=API_TOKEN)

# 1) Create an article inside a section
created = articles.create_article(
    client,
    section_id=SECTION_ID,
    article={
        "title": "Resetting your password",
        "body": "<p>Click the reset link in the login screen.</p>",
        "locale": LOCALE,
    },
    locale=LOCALE,
    notify_subscribers=False,
)
assert created is not None
article_id = created["article"]["id"]
print(f"Created article {article_id}")

# 2) Add a French translation
translations.create_translation(
    client,
    parent="articles",
    parent_id=article_id,
    translation={
        "locale": "fr",
        "title": "Reinitialiser votre mot de passe",
        "body": "<p>Cliquez sur le lien de reinitialisation.</p>",
    },
)

# 3) Search for it
results = search.search_articles(client, query="password reset", locale=LOCALE)
assert results is not None
print(f"Found {len(results.get('results', []))} matches")
