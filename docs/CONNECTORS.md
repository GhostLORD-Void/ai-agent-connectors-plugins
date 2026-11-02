# Connector setup

This repository exposes 10 service integrations as 11 MCP tools.

| Service | Tool(s) | Credential |
|---|---|---|
| GitHub | github_list_repos, github_create_issue | GITHUB_TOKEN |
| GitLab | gitlab_list_projects | GITLAB_TOKEN |
| Slack | slack_send_message | SLACK_BOT_TOKEN |
| Discord | discord_send_webhook | webhook URL per call |
| Notion | notion_search | NOTION_TOKEN |
| Jira Cloud | jira_create_issue | JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN |
| Linear | linear_create_issue | LINEAR_API_KEY |
| OpenAI | openai_chat | OPENAI_API_KEY |
| Google Gemini | gemini_generate | GEMINI_API_KEY |
| Tavily | tavily_search | TAVILY_API_KEY |

## Run
Python 3.10+ recommended. No third-party Python dependencies are required.
Run: python src/mcp_server.py
Configure an MCP client using mcp-config.example.json; replace the example path and provide secrets in that client's environment.

## Permissions
- GitHub: repository metadata read and issues write only on intended repositories.
- GitLab: read_api for project listing.
- Slack: chat:write and workspace app installation.
- Notion: internal integration shared only with selected pages.
- Jira: API token and project issue-create permission.
- Linear: API key with intended team access.
- OpenAI, Gemini, Tavily: provider API keys.
- Discord: webhook URL is a secret; pass only the intended channel webhook.

## Safety
Issue creation and messaging tools write to external services. Review tool arguments before use. The server does not print tokens. Never commit .env, webhook URLs, private keys, or customer data.
