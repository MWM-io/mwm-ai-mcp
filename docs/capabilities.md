# What MWM AI can help with

[Install](installation.md) · [Example prompts](examples.md)

MWM combines hosted tools with workflow skills. Operations available in a
conversation depend on connected accounts, app ownership, your role, assistant
settings, and data coverage. The live service describes its available tools;
this page groups the workflows rather than fixing a tool count.

| Area | Examples |
| --- | --- |
| Market research | Discover competitors, compare keywords and charts, inspect review themes, observed ads, paywalls, and onboardings |
| Store copy | Draft and localize names, subtitles, keywords, descriptions, promotional text, and release notes; review listing text |
| Store visuals | Create and refine icons, screenshot concepts, screenshots, variants, and localized assets |
| Brand | Read and maintain an app's brand guide and visual references |
| Acquisition pages | Prepare App Store custom product pages, Google Play custom listing drafts, and app landing pages |
| Privacy and legal | Prepare policies and terms from MWM's clause library; help with Data safety, App Privacy, account deletion, and trader information |
| Releases | Inspect release status, prepare App Store versions and submissions, manage supported release steps, and publish an existing signed Android build to a track |
| Live moments | Prepare App Store in-app events and Google Play promotional content |
| Reviews | Analyze your App Store ratings and reviews; draft and publish developer replies where authorized |
| App analytics | Read and compare supported revenue, users, retention, cohorts, and lifetime value |
| Publishing knowledge | Retrieve store guidance and MWM definitions with sources and checked dates |

## Boundaries that matter

- **iOS binaries:** the plugin does not build, sign, or upload an IPA. Use your
  normal build pipeline for those steps.
- **Android builds:** publishing uses an existing signed build; generating a
  signed application from source is a separate workflow.
- **Store differences:** a Google Play custom listing or promotional-content
  draft does not imply automatic Play Console submission. Check the returned
  state and handoff instructions.
- **App Privacy:** the skill can help inspect your code and guide a signed-in
  browser when your client provides those capabilities. MCP alone does not
  grant filesystem or browser access.
- **Research:** results reflect the available market data and its freshness;
  keyword and opportunity metrics are estimates.
- **Legal and store review:** generated content and assembled documents do not
  guarantee legal compliance or acceptance by Apple or Google.
- **Rendering:** interactive panels and rich media vary by host. Check your
  client's support for the workflow you need.

Ask for a draft or preview when you want to review an outcome. Publishing,
submission, and externally visible changes follow your instructions, access,
and assistant settings. Verify the returned result before treating a change as
live.

See [the thirteen bundled skills](../plugins/mwm-ai/README.md) and
[account setup](account-and-access.md).
