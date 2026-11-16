# Troubleshooting

[Installation](installation.md) · [Account setup](account-and-access.md)

## Installed, but no MWM tools

Installing the package and connecting the account are different steps.

1. Verify you installed **MWM AI**, rather than only registering its marketplace.
2. Open the client's MCP or connector controls and enable the MWM server.
3. Select **Connect**, **Authenticate**, or the equivalent sign-in action.
4. Finish browser authorization and return to the client.
5. Restart the server or start a new conversation, then request a knowledge lookup.

In Codex desktop, check **Settings → MCP servers → Authenticate**. In Claude
Code, inspect `/mcp`. See your [client guide](installation.md) for other hosts.

## Sign-in loops or a 401 response

Check that the URL is exactly `https://mcp.mwm.ai/mcp`, with no added query
parameters or alternate hostname. Remove manually added Authorization headers
and use the client's OAuth flow. A 401 before authorization is part of OAuth
discovery; a browser GET alone does not test MCP connectivity.

Disconnect and reconnect the MWM server if authorization remains stale. Keep
the account and organization consistent throughout sign-in. If it still fails,
record the client version, time, and sanitized error message for support.

## Signed in, but my apps are missing

Check the MWM account and organization you authorized, your role, and the store
connection in Console. Signing in to the assistant does not connect App Store
Connect or Google Play. Ask MWM AI to check store connection status and follow
the organization-specific Console links.

## Duplicate servers or repeated tools

A plugin installation and a manual MCP server can load MWM twice. Keep one
route per client. Remove the manual server or uninstall the duplicate plugin,
then restart or begin a new chat. A plugin-provided server can have a longer
host-generated name containing `mwm-ai`; that alone is normal.

## Switch from the private marketplace

The earlier internal and public catalogs both use marketplace name `mwm`.
Clients may refuse two sources with the same name. For a move to the public
production source, remove the old registration and add the new one.

Claude Code:

```bash
claude plugin uninstall mwm-ai@mwm
claude plugin marketplace remove mwm
claude plugin marketplace add MWM-io/mwm-ai-mcp
claude plugin install mwm-ai@mwm
```

Codex CLI:

```bash
codex plugin remove mwm-ai@mwm
codex plugin marketplace remove mwm
codex plugin marketplace add MWM-io/mwm-ai-mcp
codex plugin add mwm-ai@mwm
```

These steps change your local source of updates. They do not connect store
accounts or transfer permissions. For simultaneous internal testing, use a
separate client profile rather than replacing the production source repeatedly.

## ZIP upload does not work

Use the artifact for your host from
[releases](https://github.com/MWM-io/mwm-ai-mcp/releases):

| Artifact | Intended use |
| --- | --- |
| `mwm-ai-plugin-claude-<version>.zip` | Claude custom plugin upload |
| `mwm-ai-plugin-<version>.zip` | Codex desktop compatibility package |
| `mwm-ai-plugin-submission-<version>.zip` | OpenAI submission portal; maintainer artifact |

The GitHub source ZIP has a repository wrapper and is not an installable plugin
ZIP. After successful upload, complete the separate MWM authorization.

## Generation times out or a panel does not render

Some creative operations take longer than a chat response. Inspect the result
or task status before repeating a paid operation. An interrupted client does
not prove that the service did no work. Interactive panels and rich previews
depend on the host; use text or returned result links where supported.

## Updates do not appear

Refresh the repository marketplace, update the installed plugin, and start a
new session. ZIP copies require importing a newer ZIP. A directory listing
and MWM's GitHub marketplace have separate distribution and review schedules;
publishing to GitHub alone does not update a reviewed store listing.

## Remove access

Uninstall the plugin or remove the manual MCP server in your client. Disconnect
the MWM account connection there as well when you want to revoke its access.
Manage App Store Connect and Google Play integrations separately in Console.

For unresolved account or connection issues, email
[support@mwm.ai](mailto:support@mwm.ai). Never include passwords, tokens,
service-account files, private app data, or store keys in public issues.
