from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.support import side_conversations

SUBDOMAIN = "your_subdomain"
EMAIL = "you@company.com"
API_TOKEN = "your_api_token"

PARENT_TICKET_ID = 11111
GROUP_ID = 2222222222  # support_group_id for the child ticket assignment

client = ZendeskClient(subdomain=SUBDOMAIN, email=EMAIL, token=API_TOKEN)

resp = side_conversations.create_child_ticket(
    client=client,
    parent_ticket=PARENT_TICKET_ID,
    subject="Follow-up from parent ticket",
    body="<p>Please handle this child ticket.</p>",
    assigned_group=GROUP_ID,
    html=True,
    custom_fields=[{"id": 1234567890, "value": "foo"}],
)
print(resp)
