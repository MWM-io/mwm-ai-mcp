# VS Code and GitHub Copilot

[All clients](../installation.md) · [Troubleshooting](../troubleshooting.md)

Add MWM AI as a remote HTTP MCP server. This gives Copilot access to MWM tools
without installing the Claude/Codex plugin's skills.

## Add the server

1. Open a local project folder, enable AI features, and select **Copilot** as
   the session target.
2. Run **MCP: Add Server** from the Command Palette.
3. Choose **HTTP** and enter `https://mcp.mwm.ai/mcp`.
4. Use **mwm-ai** as the server ID.
5. Choose the configuration scope you want. Current Copilot versions offer
   **Global → Copilot Global** for personal setup.
6. Review the server trust prompt, start the server, and complete MWM OAuth
   sign-in when requested.

You can also use **Chat: Open Customizations → MCP Servers → Add Server**.
Use the client-generated configuration for your harness: Copilot and older VS
Code Local configurations can use different files and schemas.

## Verify

Ask in an agent chat:

> Use the MWM AI MCP tools to retrieve a publishing knowledge topic and cite
> its source and checked date. Do not modify my apps.

Expand the tool call to confirm it used MWM. If the server runs but its tools
are absent, check tool enablement and the server output in MCP settings.

## Remove

Open **Chat: Open Customizations → MCP Servers**, find MWM AI, and use its
**Disable** or **Uninstall** control. If it was supplied by a shared workspace
configuration, manage that configuration with your team.

Sources: [VS Code's MCP setup guide](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
and the configuration reference linked from that guide. This configuration
follows documented client support; full MWM workflows still need verification
in your client version.
