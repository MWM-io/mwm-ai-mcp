# Changelog

## 0.32.4 — 2026-11-17

- Separate Claude's native `.mcp.json` from Codex's explicitly referenced
  `.mcp.codex.json`, so the repository itself meets Claude's directory allowlists.
- Keep OpenAI's OAuth metadata, scopes, onboarding, interface, review cases,
  version header, and Codex tool timeout in the OpenAI distribution.
- Generate the portable root `mcp.json` only for the OpenAI submission ZIP.
- Remove directory-only privacy metadata from Claude's manifest as requested
  by review; the privacy URL remains in the OpenAI manifest and documentation.
- Add regression checks for Claude's remote MCP, OAuth, and `package.json`
  field lists and for all three package formats.

## 0.32.3 — 2026-11-16

First release prepared for the public `MWM-io/mwm-ai-mcp` distribution.

- Publish the plugin, skills, distribution scripts, and documentation under MIT.
- Add installation guides for ChatGPT, Claude web/Desktop/Cowork, Claude Code,
  Codex, Cursor, VS Code/GitHub Copilot, Gemini CLI, and other MCP clients.
- Explain OAuth, store connections, client compatibility, updates, and removal.
- Separate native Claude metadata from Codex/OpenAI metadata.
- Add a Claude-specific ZIP and include the license and Claude icon in packages.
- Keep the thirteen workflow skills and production MCP endpoint; fix a research
  skill sentence that failed the existing packaging lint.
