# MWM AI plugin

The installable package for MWM's hosted MCP service. It includes thirteen
workflow skills, three commands, icons, and MCP connection metadata.
The production endpoint is `https://mcp.mwm.ai/mcp`; no local server or runtime
is required.

For installation instructions, examples, and troubleshooting, see the
[MWM AI repository](https://github.com/MWM-io/mwm-ai-mcp).

## Connect after installing

Ask **“Help me connect MWM AI and check that its tools are available.”**
If sign-in does not open, use your client's **Connect** or **Authenticate**
control for the MWM MCP server. Complete browser authorization and start a new
conversation if the tools have not refreshed.

MWM authorization and store account connections are separate steps. Connect
App Store Connect and Google Play in [MWM Console](https://console.mwm.ai)
when you want to work on your own apps.

## Contents

| Path | Purpose |
| --- | --- |
| `.claude-plugin/plugin.json` | Native Claude plugin manifest |
| `.claude-plugin/icon.png` | Claude directory icon |
| `.codex-plugin/plugin.json` | Codex manifest and OpenAI interface metadata |
| `.mcp.json` | Shared desktop connection configuration |
| `mcp.json` | Portable MCP configuration used by the OpenAI submission builder |
| `skills/setup/` | Account connection, missing tools, and store setup |
| `skills/working-with-mwm/` | Shared work, briefs, roles, and user intent |
| `skills/store-copy/` | Store listing text and localization |
| `skills/store-visuals/` | Icons, screenshots, headers, and store graphics |
| `skills/brand-visuals/` | Brand guidance and visual references |
| `skills/acquisition-pages/` | Custom product pages, custom listings, and landing pages |
| `skills/privacy-and-legal/` | Policies, terms, Data safety, deletion, and trader information |
| `skills/app-privacy/` | App Store App Privacy answers |
| `skills/shipping/` | Builds, versions, review, tracks, and releases |
| `skills/live-moments/` | Store events and promotional content |
| `skills/reviews/` | Ratings, review themes, and developer replies |
| `skills/market-research/` | Competitors, keywords, charts, ads, and captured flows |
| `skills/app-analytics/` | Revenue, users, retention, cohorts, and lifetime value |
| `commands/` | Creative and store-copy command entry points |
| `assets/` | MWM AI icon |
| `LICENSE` | MIT license for the package |

The skills hold workflow judgment. Current store facts come from tool results
and MWM's publishing knowledge base with their sources and checked dates.
The live server describes which tools are available to the connected account.

## Commands

In Claude Code, commands are namespaced by the plugin:

- `/mwm-ai:generate-app-icons`
- `/mwm-ai:generate-store-screenshots`
- `/mwm-ai:write-store-text`

Hosts can expose the same workflows through their own skill controls.
A direct MCP-only connection does not install these commands or skills.

## Compatibility with earlier skill names

| Old name | Pack |
| --- | --- |
| store-text, write-store-text, store-listing | store-copy |
| store-screenshots, generate-store-screenshots, app-icons, generate-app-icons | store-visuals |
| custom-product-pages, play-custom-listings, landing-page | acquisition-pages |
| app-store-events, play-promotional-content | live-moments |
| store-publish, store-release | shipping |
| legal-documents, legal-and-web | privacy-and-legal |
| market-intelligence, market-and-keywords | market-research |
| setup, store-connection | setup |
| working-with-mwm, store-copy, store-visuals, brand-visuals, app-privacy, acquisition-pages, live-moments, shipping, reviews, app-analytics | unchanged name |

## Distribution formats

The Claude ZIP contains the native Claude manifest and a Claude MCP
configuration. The desktop ZIP includes the Claude and Codex manifests and
the shared desktop MCP configuration. The OpenAI submission ZIP uses a
generated root `plugin.json` and portable `mcp.json`.

Manifests share the plugin identity and version, while keeping host-specific
metadata in the appropriate manifest. The desktop version header
`X-MWM-Plugin-Version` identifies the installed package to the service; it
is not a credential. No account token is included in the package.

## Access, usage, and support

Your MWM role, assistant settings, connected accounts, and available service
features determine what you can do. Creative generation may use MWM credits.
Client support determines whether interactive panels and rich media render.

[Support](mailto:support@mwm.ai) ·
[Privacy](https://console.mwm.ai/mcp/privacy) ·
[Terms](https://mwm.ai/terms-of-service) · [MIT license](LICENSE)
