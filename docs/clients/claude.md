# Claude web, Desktop, and Cowork

[All clients](../installation.md) · [Claude Code](claude-code.md)

## Install the plugin from MWM's marketplace

In Claude, open **Customize → Plugins** and the marketplace controls. Add this
public repository as a marketplace:

```text
https://github.com/MWM-io/mwm-ai-mcp
```

Find **MWM AI** in that marketplace and add it. In Cowork, open the Cowork tab
before Customize. If repository marketplaces are restricted by your
organization, ask its owner to allow or distribute the plugin.

You can also upload the Claude plugin ZIP from the repository's
[releases](https://github.com/MWM-io/mwm-ai-mcp/releases), when available, through
the custom plugin upload control. Use the artifact named
`mwm-ai-plugin-claude-<version>.zip`. Upload the ZIP itself, rather than the
GitHub source archive, which has a different layout.

Connect the bundled MWM connector when requested and finish MWM authorization
in your browser. Start a new conversation and ask MWM AI to verify its tools.
See [Claude's plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

These are installation routes from MWM's public distribution. They do not
indicate that Anthropic has accepted MWM AI into its directory.

## Alternative: add the remote connector

For MCP tools without bundled skills:

1. Open **Customize → Connectors → Add → Add custom connector**.
2. Name it **MWM AI** and enter `https://mcp.mwm.ai/mcp`.
3. Keep OAuth sign-in enabled. If the client asks how to identify itself,
   choose **Register automatically** for MWM's dynamic client registration.
   No manually created client ID, client secret, or request header is needed.
4. Connect, complete MWM sign-in, and enable the connector in your conversation.

On Team or Enterprise, an authorized administrator may need to add the custom
connector to the organization before members can connect individually. Follow
[Claude's custom connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
for the controls available to your account.

Use the remote connector controls for this hosted server. The Desktop local
server configuration file is a different mechanism.

## Verify, update, or remove

> Use MWM AI to retrieve a publishing knowledge topic and cite its source and
> checked date. Do not change my apps.

Check the MWM tool result. A connector installation alone does not install the
plugin's skills. If you upload a ZIP, upload a newer ZIP to update that copy;
marketplace and directory copies follow their own update controls. Manage or
remove the plugin in Customize, and disconnect the MWM connector to revoke that
connection. See [troubleshooting](../troubleshooting.md).
