# Other MCP clients

[All clients](../installation.md) · [Troubleshooting](../troubleshooting.md)

MWM's hosted MCP service can be configured in a client that supports:

- **Streamable HTTP** remote MCP transport.
- OAuth browser sign-in, protected-resource discovery, and dynamic client
  registration as a public client.
- The MCP tools needed for your workflow.

Use server name `mwm-ai` and endpoint `https://mcp.mwm.ai/mcp`. Let the
client discover OAuth settings. Sign in with your own MWM account when it opens
your browser. No shared credentials or local server command is supplied by
this repository.

Some clients use this shape:

```json
{
  "mcpServers": {
    "mwm-ai": {
      "url": "https://mcp.mwm.ai/mcp"
    }
  }
}
```

This is an example, not a universal configuration. A client may instead require
`servers`, `httpUrl`, TOML, or a settings form. Follow its official remote
MCP documentation. If it only supports stdio or cannot complete OAuth, this
direct connection is not sufficient.

Clients such as Windsurf/Devin, Cline, or other agents should be assessed using
their current documentation. A model's name alone does not establish MCP or
plugin support. Do not assume the Claude/Codex plugin can be imported into a
different host.

After connecting, ask for an MWM publishing knowledge lookup and inspect the
actual tool result. Check private app access separately. Interactive panels,
resources, media rendering, uploads, and long-running operations depend on
client support; test the workflows you need before relying on them.

Protocol reference: [MCP authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization).
