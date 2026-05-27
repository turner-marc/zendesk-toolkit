# Zendesk API Python Library — Function Reference

## Layout

```python
from zendesk_toolkit import ZendeskClient, ZendeskError
from zendesk_toolkit.support import tickets, users, ...
from zendesk_toolkit.help_center import articles, sections, ...
```

## Client (shared)
| Function | Description |
|-----------|-------------|
| `ZendeskClient(subdomain, email, token)` | Create a new API client (Basic Auth) |
| `ZendeskClient(subdomain, oauth_token=...)` | Create a client with OAuth bearer token |
| `.get(endpoint, params)` | GET request |
| `.post(endpoint, json, files)` | POST request |
| `.put(endpoint, json)` | PUT request |
| `.patch(endpoint, json)` | PATCH request |
| `.delete(endpoint)` | DELETE request |
| `ZendeskError` | Exception with `.status`, `.request_id`, `.payload` |

---

# Support API (`zendesk_toolkit.support`)

## Tickets
| Function | Description |
|-----------|-------------|
| `create_ticket(client, ticket)` | Create new ticket |
| `get_ticket(client, id)` | Retrieve a ticket |
| `update_ticket(client, id, ticket)` | Update ticket fields |
| `add_comment_with_uploads(client, id, body, upload_tokens, custom_fields, extra_updates)` | Add comment + uploads + field updates |
| `bulk_update(client, ids, changes)` | Bulk update tickets |
| `merge_tickets(client, target_id, source_ids)` | Merge tickets |
| `list_ticket_audits(client, id)` | Ticket audit trail |
| `list_ticket_metrics(client, id)` | Ticket metrics |
| `incremental_tickets_cursor(client, start_time, cursor)` | Incremental export (cursor) |

## Uploads
| Function | Description |
|-----------|-------------|
| `upload_file(client, filename, file_bytes, content_type)` | Upload attachment |

## Users
| Function | Description |
|-----------|-------------|
| `create_user(client, user)` | Create user |
| `get_user(client, id)` | Get user |
| `update_user(client, id, user)` | Update user |
| `delete_user(client, id)` | Delete user |
| `search_users_by_email(client, email)` | Find users by email |
| `search_users(client, query)` | Search users via Search API |
| `get_agents(client, include_admin)` | List agents/admins |
| `list_user_identities(client, id)` | List user identities |

## Organizations
| Function | Description |
|-----------|-------------|
| `list_organizations(client)` | List all organizations |
| `get_organization(client, id)` | Get organization |
| `create_organization(client, org)` | Create organization |
| `update_organization(client, id, org)` | Update organization |
| `delete_organization(client, id)` | Delete organization |
| `search_organizations(client, name)` | Search orgs by name |
| `list_org_memberships(client, id)` | List memberships |

## Groups
| Function | Description |
|-----------|-------------|
| `list_groups(client)` | List groups |
| `get_group(client, id)` | Get group |
| `create_group(client, group)` | Create group |
| `update_group(client, id, group)` | Update group |
| `delete_group(client, id)` | Delete group |
| `list_group_memberships(client, id)` | List group members |
| `list_assignable_groups(client)` | List assignable groups |

## Macros
| Function | Description |
|-----------|-------------|
| `list_macros(client)` | List macros |
| `get_macro(client, id)` | Get macro |
| `apply_macro(client, mid, ticket_id)` | Apply macro to ticket |
| `list_macro_definitions(client)` | List macro definitions |

## Views
| Function | Description |
|-----------|-------------|
| `list_views(client)` | List all views |
| `get_view(client, id)` | Get a view |
| `execute_view(client, id)` | Execute a view |
| `view_count(client, id)` | Get view ticket count |
| `preview_view(client, criteria)` | Preview a custom view |

## Custom Fields
| Function | Description |
|-----------|-------------|
| Ticket Fields | list, get, create, update, delete |
| User Fields | list, get, create, update, delete |
| Organization Fields | list, get, create, update, delete |

## Side Conversations
| Function | Description |
|-----------|-------------|
| `create_child_ticket(client, parent_ticket, subject, body, assigned_group, html, custom_fields)` | Create a side conversation child ticket |

## Search
| Function | Description |
|-----------|-------------|
| `search(client, query)` | General search across resources |

---

# Help Center API (`zendesk_toolkit.help_center`)

Most resource functions accept an optional `locale=` kwarg. When provided, the request goes to the `/help_center/{locale}/...` URL variant; when omitted, the agent-only `/help_center/...` variant is used.

## Articles
| Function | Description |
|-----------|-------------|
| `list_articles(client, locale, params)` | List all articles |
| `get_article(client, article_id, locale)` | Show article |
| `create_article(client, section_id, article, locale, notify_subscribers)` | Create article in a section |
| `update_article(client, article_id, article, locale)` | Update article |
| `archive_article(client, article_id, locale)` | Archive (DELETE) article |
| `update_article_source_locale(client, article_id, source_locale)` | Change source locale |
| `list_articles_by_category(client, category_id, locale, params)` | Articles in a category |
| `list_articles_by_section(client, section_id, locale, params)` | Articles in a section |
| `list_articles_by_user(client, user_id, params)` | Articles authored by a user |
| `incremental_articles(client, start_time, params)` | Incremental export |

## Categories
| Function | Description |
|-----------|-------------|
| `list_categories(client, locale, params)` | List categories |
| `get_category(client, category_id, locale)` | Show category |
| `create_category(client, category, locale)` | Create category |
| `update_category(client, category_id, category, locale)` | Update category |
| `delete_category(client, category_id, locale)` | Delete category |
| `update_category_source_locale(client, category_id, source_locale)` | Change source locale |

## Sections
| Function | Description |
|-----------|-------------|
| `list_sections(client, locale, params)` | List sections |
| `get_section(client, section_id, locale)` | Show section |
| `create_section(client, category_id, section, locale)` | Create section in a category |
| `update_section(client, section_id, section, locale)` | Update section |
| `delete_section(client, section_id, locale)` | Delete section |
| `list_sections_by_category(client, category_id, locale, params)` | Sections in a category |
| `update_section_source_locale(client, section_id, source_locale)` | Change source locale |

## Translations
`parent` must be one of `"articles"`, `"sections"`, `"categories"`.

| Function | Description |
|-----------|-------------|
| `list_translations(client, parent, parent_id, params)` | List translations of an article/section/category |
| `list_missing_translations(client, parent, parent_id)` | List missing locales |
| `get_translation(client, parent, parent_id, locale)` | Show translation |
| `create_translation(client, parent, parent_id, translation)` | Create translation |
| `update_translation(client, parent, parent_id, locale, translation)` | Update translation |
| `delete_translation(client, translation_id)` | Delete translation |

## Article Attachments
| Function | Description |
|-----------|-------------|
| `list_article_attachments(client, article_id, kind=None)` | List article attachments; `kind` may be `"block"` or `"inline"` |
| `get_article_attachment(client, attachment_id)` | Show attachment |
| `create_article_attachment(client, article_id, guide_media_id, inline)` | Attach an existing Guide media object |
| `delete_article_attachment(client, attachment_id)` | Delete attachment |
| `bulk_attachments(client, article_id, attachment_ids)` | Associate multiple attachments |

## Article Comments
| Function | Description |
|-----------|-------------|
| `list_article_comments(client, article_id, params)` | List comments |
| `get_article_comment(client, article_id, comment_id)` | Show comment |
| `create_article_comment(client, article_id, comment)` | Create comment |
| `update_article_comment(client, article_id, comment_id, comment)` | Update comment |
| `delete_article_comment(client, article_id, comment_id)` | Delete comment |
| `upvote_article_comment(client, article_id, comment_id)` | Upvote |
| `downvote_article_comment(client, article_id, comment_id)` | Downvote |
| `list_article_comment_votes(client, article_id, comment_id)` | List comment votes |
| `list_comments_by_user(client, user_id)` | Comments authored by a user |

## Labels
| Function | Description |
|-----------|-------------|
| `list_all_labels(client, params)` | List all labels |
| `get_label(client, label_id)` | Show label |
| `delete_label(client, label_id)` | Delete label |
| `list_article_labels(client, article_id)` | List an article's labels |
| `create_article_label(client, article_id, name)` | Add a label to an article |
| `delete_article_label(client, article_id, label_id)` | Remove a label from an article |

## Votes
| Function | Description |
|-----------|-------------|
| `get_vote(client, vote_id)` | Show vote |
| `delete_vote(client, vote_id)` | Delete vote |
| `list_article_votes(client, article_id)` | List article votes |
| `upvote_article(client, article_id)` | Upvote article |
| `downvote_article(client, article_id)` | Downvote article |
| `list_user_votes(client, user_id)` | Votes cast by a user |

## Search
| Function | Description |
|-----------|-------------|
| `search_articles(client, query, **filters)` | Article search (at least one of `query`, `category`, `section`, `label_names` required) |
| `unified_search(client, query, **filters)` | Unified Guide search across articles/community |

## Locales
| Function | Description |
|-----------|-------------|
| `list_locales(client)` | List enabled Help Center locales |

## User Segments
| Function | Description |
|-----------|-------------|
| `list_user_segments(client, params)` | List user segments |
| `list_applicable_segments(client)` | List segments applicable to the current user |
| `get_user_segment(client, segment_id)` | Show segment |
| `create_user_segment(client, segment)` | Create segment |
| `update_user_segment(client, segment_id, segment)` | Update segment |
| `delete_user_segment(client, segment_id)` | Delete segment |
| `list_segment_sections(client, segment_id)` | Sections restricted to this segment |
| `list_segment_topics(client, segment_id)` | Topics restricted to this segment |
| `list_segments_by_user(client, user_id)` | Segments a user belongs to |

---

## Pagination (shared)
| Function | Description |
|-----------|-------------|
| `paginate_offset(client, endpoint, params)` | Iterate offset-based endpoints |
| `paginate_cursor(client, endpoint, params)` | Iterate cursor-based endpoints |
