# Install MWM AI

Choose the **application**, rather than the model name. For example, Claude in
Cursor uses Cursor's MCP settings; it does not use Claude Desktop's settings.

| Application | Recommended route | Alternative |
| --- | --- | --- |
| [ChatGPT web, desktop, mobile](clients/chatgpt.md) | MWM AI in the Plugins directory | Follow OpenAI's current custom plugin flow if your workspace requires it |
| [Claude web, Desktop, Cowork](clients/claude.md) | Add MWM's public marketplace or upload the Claude ZIP | Custom remote connector |
| [Claude Code](clients/claude-code.md) | MWM's public plugin marketplace | Direct HTTP MCP connection |
| [Codex desktop and CLI](clients/codex.md) | Plugins directory or MWM's public marketplace | Direct HTTP MCP connection; also usable from the IDE extension |
| [Cursor](clients/cursor.md) | Remote MCP configuration | — |
| [VS Code / GitHub Copilot](clients/vscode.md) | HTTP MCP server | — |
| [Gemini CLI](clients/gemini-cli.md) | HTTP MCP server | JSON settings |
| [Other clients](clients/other-clients.md) | Streamable HTTP + OAuth | Check the host's documentation |

The configuration guides were checked against the linked official client
documentation on **16 November 2026**. Client support and menus can change.
The documented MCP routes for Cursor, Copilot, Gemini CLI, and other clients
describe compatible client configuration; they are not a claim that every
MWM workflow has been tested end to end in those hosts.

## Before you connect

- Have an MWM account and use the account that has access to your organization.
- Use a client with **remote Streamable HTTP** and **OAuth** support.
- Allow the browser to open for MWM sign-in and return to your assistant.
- If your workspace controls integrations, have an administrator make MWM AI
  available. Each person still connects with their own MWM identity.

No MWM API key, shared password, Node.js package, or local server is needed.
The production URL is exactly:

```text
https://mcp.mwm.ai/mcp
```

## Check the connection

After installing and authorizing, start a new conversation:

> Use MWM AI to retrieve a publishing knowledge topic and show its source and
> checked date. Do not change my apps or generate paid assets.

Expand the tool result and confirm it came from MWM. A plausible answer without
an MWM tool call does not establish that the connection works. A knowledge
lookup does not verify access to your private apps; for that, continue with
[account and store setup](account-and-access.md).

If the server is absent, authentication fails, or you see duplicate tools, use
[troubleshooting](troubleshooting.md).
