# Contributing

Thanks for helping improve AI Agent Connectors & Plugins.

## Add a connector
1. Open an issue describing the service, use case, and intended permissions.
2. Create a focused directory under connectors/<category>/<service>/.
3. Include a README, license information for copied dependencies, tests, and a runnable example.
4. Add or update the catalog entry and clearly set its status.
5. Submit a pull request with test results and known limitations.

## Quality expectations
- Keep credentials out of source control; provide .env.example with placeholders only.
- Validate inputs and return actionable, non-secret error messages.
- Use least-privilege permissions and document every requested scope.
- Include timeouts, pagination, retry/backoff, and rate-limit handling where applicable.
- Add tests; do not make live paid API calls in ordinary CI.
- Pin or constrain dependencies and document supported runtime versions.
- Respect upstream terms, licenses, privacy requirements, and API policies.

## Pull request checklist
- [ ] Documentation and setup instructions are complete.
- [ ] Tests pass, or limitations are explained.
- [ ] No secrets, personal data, or generated credentials are included.
- [ ] Permissions and data handling are documented.
- [ ] Catalog status is accurate.
