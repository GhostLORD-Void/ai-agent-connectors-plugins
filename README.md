# AI Agent Connectors & Plugins

Open community hub for reusable AI-agent connectors, tools, plugins, and MCP servers.

## Working starter integrations

10 service integrations are implemented and exposed as 11 MCP tools: GitHub (repository listing and issue creation), GitLab (project listing), Slack (message send), Discord (webhook send), Notion (search), Jira (issue creation), Linear (issue creation), OpenAI (chat completion), Google Gemini (content generation), and Tavily (web search).

**Status:** API clients, MCP stdio server, and local mocked tests are included. Live API calls require your credentials and have not yet been verified against your accounts.

## Quick start
Run: python src/mcp_server.py
No third-party Python packages are required. Configure your MCP client with mcp-config.example.json. See docs/CONNECTORS.md for setup and permissions.

## Layout
- src/connectors.py — API clients and tool registry.
- src/mcp_server.py — MCP JSON-RPC stdio server.
- tests/ — local mocked tests.
- catalog/ — ecosystem index.
- templates/ — connector template.

## Test
Run: python -m unittest discover -s tests -v

## Security
Never commit tokens, webhook URLs, private keys, .env, or customer data. Use least-privilege credentials. Write tools perform external actions. Read SECURITY.md.

## Contributing
See CONTRIBUTING.md. Mark connector status as planned, experimental, stable, or deprecated.

## License
MIT.

## Advanced build
- OAuth 2.0 helper: src/oauth_manager.py (generic client-credentials / refresh-token flow, in-memory cache).
- Dynamic connector discovery: MCP resource connectors://catalog.
- MCP resources: connectors://catalog and connectors://setup.
- MCP prompts: plan_connector and review_tool_call.
- Optional LangChain / CrewAI adapters: src/adapters/ (install requirements-optional.txt).
- Docker image: docker build -t ai-agent-connectors-plugins .
- CI: GitHub Actions workflow in .github/workflows/ci.yml.
