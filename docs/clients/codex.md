# Codex desktop, CLI, and IDE extension

[All clients](../installation.md) · [ChatGPT](chatgpt.md)

## Install the plugin

In the desktop app, open **Plugins**, search for **MWM AI**, check the MWM
publisher, and install it. Connect your MWM account when prompted. In Codex CLI,
`/plugins` opens the plugin browser.

You can also install the public repository marketplace from your terminal:

```bash
codex plugin marketplace add MWM-io/mwm-ai-mcp
codex plugin add mwm-ai@mwm
```

Start a new session to load the skills and tools. If authentication did not
start automatically, open **Settings → MCP servers** in the desktop app and
select **Authenticate** for MWM. Finish MWM authorization in the browser.

For ZIP import, use `mwm-ai-plugin-<version>.zip` from
[releases](https://github.com/MWM-io/mwm-ai-mcp/releases), when available.
The ZIP installs the package but may still require the separate Authenticate
step. See [OpenAI's plugin guide](https://learn.chatgpt.com/docs/plugins).

The IDE extension does not install plugins. Use a supported plugin surface,
or configure the MCP server directly as described below.

## Connect only the MCP server

In your terminal:

```bash
codex mcp add mwm-ai --url https://mcp.mwm.ai/mcp
codex mcp login mwm-ai
```

Complete browser sign-in. Check the server with `codex mcp list`, then start
Codex and use `/mcp`. The direct server includes tools without installing skills.

For a configuration file instead, merge this into `~/.codex/config.toml`:

```toml
[mcp_servers.mwm-ai]
url = "https://mcp.mwm.ai/mcp"
tool_timeout_sec = 900
```

Then run `codex mcp login mwm-ai`. Local Codex clients using the same host
configuration can share this setup; ChatGPT web does not read the file. In the
IDE extension, the MCP settings also offer **Add server** and **Authenticate**.
See [OpenAI's MCP guide](https://learn.chatgpt.com/docs/extend/mcp).

## Verify, update, and remove

> Use MWM AI to check a publishing knowledge topic and cite its source and date.
> Do not change my apps.

Check the actual tool result. To refresh a repository installation:

```bash
codex plugin marketplace upgrade mwm
codex plugin add mwm-ai@mwm
```

Start a new session. To uninstall the repository plugin, run
`codex plugin remove mwm-ai@mwm`. For a manual MCP connection, use
`codex mcp logout mwm-ai` and `codex mcp remove mwm-ai`.

Use one route per client to avoid duplicate servers. If you used the earlier
private marketplace, follow the
[migration guide](../troubleshooting.md#switch-from-the-private-marketplace).
