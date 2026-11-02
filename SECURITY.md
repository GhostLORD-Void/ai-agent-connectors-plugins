# Security Policy

Do not report vulnerabilities in public issues. Use GitHub's private vulnerability reporting for this repository if enabled, or contact the repository maintainers privately.

## Connector security baseline
- Never store tokens or passwords in source code, logs, fixtures, or committed configuration.
- Use least-privilege OAuth scopes and rotate credentials if exposure is suspected.
- Treat model output, tool output, web pages, and uploaded files as untrusted.
- Validate and constrain tool arguments; require confirmation for destructive actions.
- Apply timeouts, size limits, rate limits, and explicit network destination policies.
- Redact secrets and sensitive user data from logs.
