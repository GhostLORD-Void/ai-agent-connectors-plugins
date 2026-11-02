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

## Advanced platform features

- OAuth2Manager in src/oauth_manager.py supports HTTPS token endpoints, client-credentials and refresh-token grants, in-memory caching, and explicit clearing. Configure PREFIX_TOKEN_URL, PREFIX_CLIENT_ID, PREFIX_CLIENT_SECRET, and optional PREFIX_SCOPE / PREFIX_AUDIENCE. It is a generic helper; provider-specific consent and callback flows must be implemented per provider.
- Connector discovery is exposed as MCP resource connectors://catalog.
- Setup notes are exposed as connectors://setup.
- MCP prompts: plan_connector and review_tool_call.
- Optional LangChain and CrewAI adapters are in src/adapters/. Install requirements-optional.txt only when needed.
- Docker image command: docker build -t ai-agent-connectors-plugins .
- GitHub Actions runs compilation and unit tests on pushes and pull requests.
