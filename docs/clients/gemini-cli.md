# Gemini CLI

[All clients](../installation.md) · [Troubleshooting](../troubleshooting.md)

These instructions apply to **Gemini CLI**. They do not configure the Gemini
web application. The direct MCP connection provides tools without installing
the Claude/Codex plugin's skills.

## Add the server

In your terminal:

```bash
gemini mcp add --scope user --transport http mwm-ai https://mcp.mwm.ai/mcp
```

Start Gemini CLI and authenticate:

```text
/mcp auth mwm-ai
```

Complete MWM sign-in in your browser and return to the CLI. Use `/mcp` to
inspect connection status. OAuth needs a working browser callback on the
computer running the CLI.

## Configure with JSON instead

Merge this into `~/.gemini/settings.json` for user scope, or
`.gemini/settings.json` for project scope:

```json
{
  "mcpServers": {
    "mwm-ai": {
      "httpUrl": "https://mcp.mwm.ai/mcp",
      "oauth": {
        "enabled": true
      }
    }
  }
}
```

Then run `/mcp auth mwm-ai`. Use `httpUrl` for Streamable HTTP;
`url` can refer to SSE in Gemini's configuration. Let the client discover the
OAuth endpoints and register itself.

## Verify and remove

> Use MWM AI to retrieve a publishing knowledge topic and cite its source and
> checked date. Do not change my apps.

Confirm an actual tool call. To inspect or remove the user-scoped server:

```bash
gemini mcp list
gemini mcp remove --scope user mwm-ai
```

Source: [Gemini CLI MCP configuration and OAuth](https://geminicli.com/docs/tools/mcp-server/).
These are documented client settings, not an end-to-end MWM compatibility
certification for every Gemini CLI release.
