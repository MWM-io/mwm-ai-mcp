# Cursor

[All clients](../installation.md) · [Troubleshooting](../troubleshooting.md)

Connect MWM's hosted MCP server directly. This route provides MCP tools;
it does not install the Claude/Codex plugin's skills.

## Configure

Open Cursor's **Customize → MCP** controls, or edit
`~/.cursor/mcp.json` for all projects. For a single project, use
`.cursor/mcp.json`. Merge the following entry with your existing servers:

```json
{
  "mcpServers": {
    "mwm-ai": {
      "url": "https://mcp.mwm.ai/mcp"
    }
  }
}
```

Save, enable the server, and follow Cursor's OAuth connection prompt. Sign in
to MWM and return to Cursor. MWM uses automatic client registration; you do not
need to add an API key or a static OAuth client secret.

Use an agent chat with the MWM tools enabled and test:

> Use MWM AI to retrieve a publishing knowledge topic and cite its source and
> checked date. Do not change my apps.

Check that a tool result actually appears. If Cursor does not refresh the tool
list, restart the server or Cursor, then open a new agent chat.

## Manage the connection

Disable or remove the `mwm-ai` entry through Cursor's MCP controls when you
no longer want the tools available. To switch to a plugin installation later,
remove the manual server so it is not loaded twice. Account authorization is
managed separately from the configuration.

Source: [Cursor's MCP configuration and OAuth documentation](https://cursor.com/docs/mcp).
The client configuration is documented; full MWM workflow compatibility in
Cursor must be verified in the version you use.
