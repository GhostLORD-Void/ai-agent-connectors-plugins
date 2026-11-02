# AI Agent Connectors & Plugins

An open, community-driven hub for building AI agents with reusable connectors, tools, plugins, MCP servers, and provider integrations.

> **Project status:** starter repository. The catalog is a roadmap and contribution index; an entry does not imply that an integration is implemented, tested, or officially supported.

## Goals
- Connect agents to models, APIs, SaaS apps, databases, files, and developer tools.
- Provide consistent connector conventions, examples, tests, and security guidance.
- Support multiple agent frameworks and tool protocols without vendor lock-in.
- Track implementation status transparently.

## Ecosystem map

| Area | Examples to explore |
|---|---|
| Model providers | OpenAI, Anthropic, Google Gemini, AWS Bedrock, Azure AI, Mistral, Cohere, Groq, Ollama |
| Agent frameworks | LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, PydanticAI, Haystack |
| Tool protocols | Model Context Protocol (MCP), OpenAPI tools, function/tool calling |
| Developer platforms | GitHub, GitLab, Jira, Linear, Slack, Discord |
| Knowledge & productivity | Notion, Google Drive, Microsoft 365, Confluence |
| Data & storage | PostgreSQL, MySQL, SQLite, Redis, MongoDB, Elasticsearch, S3 |
| Vector search | pgvector, Pinecone, Weaviate, Qdrant, Chroma, Milvus |
| Web & research | Browser automation, search APIs, crawling, document extraction |
| Observability | OpenTelemetry, Langfuse, LangSmith, Arize Phoenix |
| Automation | n8n, Zapier, Make, webhooks, queues |

See catalog/ecosystem.json for the machine-readable starter catalog.

## Repository layout
- catalog/ — ecosystem index and integration metadata.
- connectors/ — implementations, grouped by provider or service.
- examples/ — end-to-end agent examples.
- templates/ — connector and MCP server starter templates.

## Connector conventions
Each connector should document supported operations, authentication and minimum scopes, environment variables (names only), rate limits, pagination, retries, data handling, setup, examples, and tests.
Recommended status labels: planned, experimental, stable, deprecated.

## Quick start
This repository currently contains the catalog and contribution scaffolding. Pick a service in the catalog, create a connector under connectors/, and follow templates/connector/README.md.

## Security
Never commit API keys, OAuth tokens, private keys, .env files, or customer data. Request narrow permissions. Treat tool output and retrieved documents as untrusted input. Validate arguments and constrain file, shell, network, and database access. See SECURITY.md.

## Contributing
Issues and pull requests are welcome. Read CONTRIBUTING.md and use the connector template.

## License
MIT — see LICENSE.
