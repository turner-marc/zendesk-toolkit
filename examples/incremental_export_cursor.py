import time

from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.support import tickets

SUBDOMAIN = "your_subdomain"
EMAIL = "you@company.com"
API_TOKEN = "your_api_token"

client = ZendeskClient(subdomain=SUBDOMAIN, email=EMAIL, token=API_TOKEN)

# Start with a UNIX timestamp (e.g., last 5 minutes)
start_time = int(time.time()) - 300

page = tickets.incremental_tickets_cursor(client, start_time=start_time)
assert page is not None
print(page)

# If 'links.next' present, keep going:
next_url = (page.get("links") or {}).get("next")
while next_url:
    page = client.get(next_url.replace(client.base_url + "/", ""))
    if page is None:
        break
    print(f"Fetched {len(page.get('tickets', []))} tickets")
    next_url = (page.get("links") or {}).get("next")
