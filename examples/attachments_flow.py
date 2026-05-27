from pathlib import Path

from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.support import tickets, uploads

SUBDOMAIN = "your_subdomain"
EMAIL = "you@company.com"
API_TOKEN = "your_api_token"
TICKET_ID = 12345
FILEPATH = "example.pdf"

client = ZendeskClient(subdomain=SUBDOMAIN, email=EMAIL, token=API_TOKEN)

# 1) Upload file
b = Path(FILEPATH).read_bytes()
up = uploads.upload_file(client, filename=Path(FILEPATH).name, file_bytes=b, content_type="application/pdf")
assert up is not None
upload_token = up["upload"]["token"]

# 2) Add a comment with the upload token
res = tickets.add_comment_with_uploads(
    client, ticket_id=TICKET_ID, body="See attached.", upload_tokens=[upload_token]
)
print(res)
