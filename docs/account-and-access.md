# Your MWM account and store connections

[Installation](installation.md) · [Troubleshooting](troubleshooting.md)

## Three separate connections

| Step | Purpose | Where |
| --- | --- | --- |
| Install the plugin or configure MCP | Make MWM available to your assistant | Your AI client |
| Authorize your MWM account | Let that client act with your MWM identity | Browser sign-in opened by the client |
| Connect store accounts | Grant MWM access to your own apps on the stores | MWM Console |

Signing in to Console does not automatically connect your assistant. Likewise,
an MCP connection does not create App Store Connect or Google Play credentials.

## Connect your account

Install using your [client guide](installation.md). When your assistant opens
MWM sign-in, select the account that belongs to the right organization, review
the requested access, and complete authorization. Return to the client and
refresh the server or start a new conversation if needed.

Your MWM role and assistant settings determine the operations available to you.
Connecting the account does not grant an assistant permissions you do not have.

## Connect your stores

Once the MWM tools are available, ask:

> Check my App Store Connect and Google Play connections and guide me through
> any missing setup in MWM Console.

Follow the Console links returned for your organization. Enter store credentials
only in the intended Console setup pages. Do not paste passwords, API private
keys, service-account JSON, OAuth tokens, or recovery codes into the chat.

Market research does not require connecting your own stores. Reading editable
listings, private app analytics, and publishing workflows require the relevant
account connections and permissions.

## Plan changes and usage

You can ask for an audit, concept, draft, or preview before deciding to publish.
Say which app, store, territory, language, and desired outcome you mean. Tell
your assistant when you want drafts only.

Some creative or data operations use MWM credits. Check the operation's cost
and your account's usage controls. An assistant subscription does not include
MWM credits, and installing the plugin does not guarantee a particular feature
or data set is available.

## Disconnect

Use your AI client's connection controls to disconnect MWM and remove the plugin
or manual server as needed. Store integrations are separate: manage those in
MWM Console. If the client no longer lets you manage an authorization, contact
[support@mwm.ai](mailto:support@mwm.ai) without sending credentials.

Read the [service privacy policy](https://console.mwm.ai/mcp/privacy) and
[terms](https://mwm.ai/terms-of-service) for service-specific details.
