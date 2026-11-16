<p align="center"><img src="plugins/mwm-ai/assets/mwm-ai-icon.png" width="96" height="96" alt="MWM AI" /></p>

<h1 align="center">MWM AI for your AI assistant</h1>

<p align="center">Research, create, and publish mobile apps with MWM — from the assistant you already use.</p>

<p align="center">
  <a href="https://mwm.ai">Website</a> ·
  <a href="https://console.mwm.ai">MWM Console</a> ·
  <a href="docs/installation.md">Installation guide</a> ·
  <a href="docs/examples.md">Example prompts</a> ·
  <a href="docs/troubleshooting.md">Troubleshooting</a>
</p>

MWM AI connects your assistant to mobile market research, App Store and Google
Play workflows, creative tools, and your connected app data. Ask for the result
you want: compare competitors, improve a listing, create screenshots, understand
reviews, or prepare your next release.

This repository distributes the **MWM AI plugin**, its workflow skills, and
connection guides for the hosted **MWM MCP server**. The service runs at
`https://mcp.mwm.ai/mcp`; there is no server to run on your computer.

The public repository contains selected production releases. Development and
internal testing happen separately; public updates are promoted explicitly.

## Get started

1. Choose your assistant below and install the plugin or add the MCP server.
2. Sign in with your MWM account when prompted and authorize the connection.
3. Start a new conversation and ask: **“Help me connect MWM AI and check that its
   tools are available.”**

An MWM account is required for account-backed features. Connect App Store
Connect or Google Play in [MWM Console](https://console.mwm.ai) when you want to
work on your own apps. You can start with market research without connecting
your store accounts. Your assistant subscription and MWM usage are separate;
creative generation and other paid operations may consume MWM credits.

| Assistant | Installation | What you get |
| --- | --- | --- |
| [ChatGPT](docs/clients/chatgpt.md) | Find **MWM AI** in the Plugins directory | Plugin, skills, and hosted MCP tools |
| [Claude: web, Desktop, Cowork](docs/clients/claude.md) | Add this marketplace or upload the Claude ZIP; remote connector also available | Plugin and skills, or MCP tools with the connector |
| [Claude Code](docs/clients/claude-code.md) | Install from this public GitHub marketplace | Plugin, skills, commands, and MCP tools |
| [Codex: desktop and CLI](docs/clients/codex.md) | Plugins directory or this GitHub marketplace | Plugin, skills, and MCP tools |
| [Cursor](docs/clients/cursor.md) | Add the remote MCP server | MCP tools |
| [VS Code / GitHub Copilot](docs/clients/vscode.md) | Add an HTTP MCP server | MCP tools |
| [Gemini CLI](docs/clients/gemini-cli.md) | Add an HTTP MCP server | MCP tools |
| [Other MCP clients](docs/clients/other-clients.md) | Streamable HTTP with OAuth | Depends on the client's MCP support |

**Claude Code quick install**

```bash
claude plugin marketplace add MWM-io/mwm-ai-mcp
claude plugin install mwm-ai@mwm
```

Then start Claude Code, open `/mcp`, and authenticate the MWM server if prompted.
This installs from **MWM's marketplace**. Publication in Anthropic's directory is
a separate review process; these commands do not imply a directory listing.

**Already know MCP?**

| Setting | Value |
| --- | --- |
| Server name | `mwm-ai` |
| Endpoint | `https://mcp.mwm.ai/mcp` |
| Transport | Streamable HTTP |
| Authentication | OAuth in your browser; automatic client registration |
| Local runtime | None |

See the [client-specific configurations](docs/installation.md). Different hosts
use different configuration schemas; use the example for your client.

## What you can do

| Goal | Try asking |
| --- | --- |
| Research a market | “Find competitors for a habit tracker in the US and compare their keywords and review themes.” |
| Improve store copy | “Audit my app's English listing and draft a clearer subtitle and description.” |
| Create store visuals | “Prepare an icon direction and a screenshot storyboard that match my app's brand.” |
| Reach an audience | “Draft a custom product page for my meditation campaign.” |
| Plan a store event | “Prepare an in-app event for our upcoming challenge.” |
| Understand reviews | “What are the main complaints about my latest App Store version?” |
| Understand performance | “Compare my app's revenue and retention with the previous period.” |
| Prepare a release | “Check what is missing before my next App Store submission.” |

See [capabilities and boundaries](docs/capabilities.md) and
[more example prompts](docs/examples.md). Available operations depend on your
app, connected stores, role, assistant settings, and the service's data coverage.

## Plugin or MCP connection?

The **plugin** bundles the connection with thirteen skills covering setup,
working with MWM, store copy, store visuals, brand visuals, acquisition pages,
privacy and legal, App Privacy, shipping, live moments, reviews, market research,
and app analytics. The skills give your assistant guidance for each workflow.
See the [plugin contents](plugins/mwm-ai/README.md).

An **MCP-only connection** exposes the server's tools, without automatically
installing those skills or slash commands. It is useful in clients that do not
support the MWM plugin format. Interactive panels and media previews depend on
the host; tools may also return text or structured results.

Use one installation route per client to avoid duplicate MWM servers. Installing
a plugin, authorizing your MWM account, and connecting your store accounts are
three separate steps.

## Documentation

- [Installation and compatibility](docs/installation.md)
- [Account and store connections](docs/account-and-access.md)
- [Capabilities and boundaries](docs/capabilities.md)
- [Example prompts](docs/examples.md)
- [Troubleshooting and removal](docs/troubleshooting.md)
- [Plugin contents and skills](plugins/mwm-ai/README.md)
- [Changelog](CHANGELOG.md)

## Support and security

For setup and account help, contact [support@mwm.ai](mailto:support@mwm.ai).
Report reproducible documentation or packaging issues through
[GitHub Issues](https://github.com/MWM-io/mwm-ai-mcp/issues). Include your client
and version, the installation method, and the error message, with private data
removed. Use [the security reporting instructions](SECURITY.md) for vulnerabilities.

Service policies: [privacy](https://console.mwm.ai/mcp/privacy) ·
[terms](https://mwm.ai/terms-of-service).

## License

The plugin, skills, distribution scripts, and documentation in this repository
are available under the [MIT license](LICENSE). The hosted MCP service and its
private implementation are separate from this distribution. Access to the
service follows your MWM account permissions and the service terms.
