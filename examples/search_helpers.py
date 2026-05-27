from zendesk_toolkit import ZendeskClient
from zendesk_toolkit.support import search, users

client = ZendeskClient(subdomain="your_subdomain", email="you@company.com", token="your_api_token")

print(users.search_users_by_email(client, "someone@example.com"))
print(search.search(client, 'type:ticket status:open "login issue"'))
