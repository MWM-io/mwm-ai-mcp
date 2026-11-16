# Claude Code

[All clients](../installation.md) · [Claude web and Desktop](claude.md)

## Install the plugin

Run these commands in your terminal:

```bash
claude plugin marketplace add MWM-io/mwm-ai-mcp
claude plugin install mwm-ai@mwm
```

Or run these inside Claude Code:

```text
/plugin marketplace add MWM-io/mwm-ai-mcp
/plugin install mwm-ai@mwm
```

Restart Claude Code, open `/mcp`, select the MWM server, and authenticate when
requested. Complete MWM sign-in and authorization in your browser. You get the
MCP connection, thirteen skills, and the bundled commands. Test with:

> Use MWM AI to check that the connection works, then help me research my app's
> market. Do not publish anything.

The marketplace name is `mwm`; the plugin name is `mwm-ai`. These identifiers
differ from the GitHub repository name, `mwm-ai-mcp`.

## Connect only the MCP server

If you do not want the skills and commands, add the remote server directly:

```bash
claude mcp add --scope user --transport http mwm-ai https://mcp.mwm.ai/mcp
```

Start Claude Code and use `/mcp` to authenticate. `--scope user` makes the
configuration available across your projects. Use `--scope project` instead
when you want a shareable project configuration; each teammate signs in
separately. See [Claude's MCP guide](https://code.claude.com/docs/en/mcp).

Choose either the plugin or the direct server for this client. If you switch
from a manual user-scoped server to the plugin, remove that manual entry:

```bash
claude mcp remove --scope user mwm-ai
```

## Update or uninstall

```bash
claude plugin marketplace update mwm
claude plugin update mwm-ai@mwm
```

Restart Claude Code after updating. To remove the plugin:

```bash
claude plugin uninstall mwm-ai@mwm
```

If you already use MWM's earlier private marketplace, see
[migration instructions](../troubleshooting.md#switch-from-the-private-marketplace)
before adding another marketplace named `mwm`.

Installing from MWM's repository works independently of Anthropic's directory
review. Do not substitute `@claude-plugins-official` unless MWM publishes an
installation instruction for an accepted directory listing. See
[Claude's distribution guide](https://code.claude.com/docs/en/plugins/publish).
