# ChatGPT

[All clients](../installation.md) · [Troubleshooting](../troubleshooting.md)

## Install the public plugin

1. Open the [ChatGPT Plugins directory](https://chatgpt.com/plugins).
2. Search for **MWM AI**, open its details, and verify that the publisher is MWM.
3. Select the install button and connect your MWM account when prompted.
4. Complete MWM sign-in and authorization in the browser.
5. Start a new chat. Select MWM AI using `@`, or ask for a task that uses MWM.

ChatGPT and Codex share a public plugin directory. Availability can depend on
your workspace settings and the surface indicated on the listing. If a plugin
is marked **Desktop only**, use the supported desktop app. See
[OpenAI's installation guide](https://learn.chatgpt.com/docs/plugins).

## Verify setup

> Help me connect MWM AI. Check its tools with a publishing knowledge lookup,
> then explain how to connect my store accounts.

Confirm an actual MWM tool result appears. If no connection prompt opened during
installation, open the installed plugin's connection controls and connect it
there. Installing and signing in are separate steps.

## MCP-only and custom workspace connections

For the public service, prefer the reviewed MWM AI plugin. ChatGPT web uses
MCP-backed tools through plugins; a local `mcp.json` or `~/.codex/config.toml`
does not configure ChatGPT web. Workspace administrators who need a custom
integration should follow OpenAI's
[connect-and-test guide](https://developers.openai.com/plugins/deploy/connect-chatgpt)
with `https://mcp.mwm.ai/mcp` and OAuth.

For direct MCP configuration in a local Codex host, use the
[Codex instructions](codex.md#connect-only-the-mcp-server).

## Updates and removal

Manage the plugin and its connection in the Plugins directory. After an update,
start a new conversation. Disconnect the MWM connection when you want to remove
that assistant's access; uninstalling a local package and revoking account
authorization are different operations.

See [MWM account and store access](../account-and-access.md) for the remaining
setup and [OpenAI's MCP guide](https://learn.chatgpt.com/docs/extend/mcp) for the
difference between hosted and local connections.
