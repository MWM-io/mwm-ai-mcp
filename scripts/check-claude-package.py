#!/usr/bin/env python3
"""Check the Claude directory allowlists supplied in the MWM AI review.

Validate the files Claude actually loads, not OpenAI's separately referenced
configuration. Claude's CLI validation tolerates fields its directory rejects.
"""

import argparse
import json
import sys
from pathlib import Path


MANIFEST_FIELDS = {
    "name", "displayName", "version", "description", "author", "homepage",
    "repository", "license", "keywords", "skills", "mcpServers",
}
REMOTE_FIELDS = {
    "type", "url", "headers", "timeout", "alwaysLoad", "oauth",
    "name", "title", "displayName", "description",
}
OAUTH_FIELDS = {"clientId", "callbackPort", "authServerMetadataUrl", "scopes"}
PACKAGE_FIELDS = {
    "name", "displayName", "version", "description", "keywords", "homepage",
    "bugs", "license", "author", "contributors", "maintainers", "funding",
    "repository", "private", "type", "files", "engines", "$schema",
}


def object_only(value, label):
    if type(value) is not dict:
        raise ValueError(f"{label} must be a plain JSON object")
    return value


def allowed_fields(value, allowed, label):
    object_only(value, label)
    unexpected = value.keys() - allowed
    if unexpected:
        raise ValueError(f"{label}: fields forbidden by the Claude review: {', '.join(sorted(unexpected))}")


def read_object(path):
    def reject_constant(value):
        raise ValueError(f"{path}: {value} is not a JSON value")
    return object_only(json.loads(path.read_text(), parse_constant=reject_constant), str(path))


def validate_mcp(config, label):
    allowed_fields(config, {"mcpServers"}, label)
    servers = object_only(config.get("mcpServers"), f"{label}.mcpServers")
    for name, server in servers.items():
        at = f"{label}.mcpServers.{name}"
        allowed_fields(server, REMOTE_FIELDS, at)
        if server.get("type") not in ("http", "sse"):
            raise ValueError(f"{at}: expected Claude's http or sse transport")
        if not isinstance(server.get("url"), str):
            raise ValueError(f"{at}.url must be text")
        for key in ("name", "title", "displayName", "description"):
            if key in server and not isinstance(server[key], str):
                raise ValueError(f"{at}.{key} must be text")
        if "headers" in server:
            headers = object_only(server["headers"], f"{at}.headers")
            if not all(isinstance(value, str) for value in headers.values()):
                raise ValueError(f"{at}.headers values must be text")
        if "oauth" in server:
            oauth = server["oauth"]
            allowed_fields(oauth, OAUTH_FIELDS, f"{at}.oauth")
            for key in ("clientId", "authServerMetadataUrl"):
                if key in oauth and not isinstance(oauth[key], str):
                    raise ValueError(f"{at}.oauth.{key} must be text")
            if "callbackPort" in oauth and type(oauth["callbackPort"]) is not int:
                raise ValueError(f"{at}.oauth.callbackPort must be an integer")
            if "scopes" in oauth and (not isinstance(oauth["scopes"], list)
                                      or not all(isinstance(scope, str) for scope in oauth["scopes"])):
                raise ValueError(f"{at}.oauth.scopes must be a text array")


def validate_package_json(value, label):
    allowed_fields(value, PACKAGE_FIELDS, label)
    if "engines" in value:
        engines = object_only(value["engines"], f"{label}.engines")
        if any(not isinstance(version, str) or not version.strip() for version in engines.values()):
            raise ValueError(f"{label}.engines must contain plain version strings")


def validate(plugin):
    plugin = Path(plugin).resolve()
    manifest = read_object(plugin / ".claude-plugin/plugin.json")
    allowed_fields(manifest, MANIFEST_FIELDS, "Claude plugin.json")
    # Claude loads the default file even if mcpServers names another path.
    paths = {plugin / ".mcp.json"}
    declared = manifest.get("mcpServers")
    if declared is not None:
        if not isinstance(declared, str) or not declared.startswith("./"):
            raise ValueError("This package must declare a relative Claude MCP file")
        path = (plugin / declared).resolve()
        if not path.is_relative_to(plugin):
            raise ValueError("Claude MCP path must stay inside the package")
        paths.add(path)
    for path in paths:
        validate_mcp(read_object(path), str(path.relative_to(plugin)))
    for path in plugin.rglob("package.json"):
        validate_package_json(read_object(path), str(path.relative_to(plugin)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin", type=Path, nargs="?", default=Path(__file__).resolve().parents[1] / "plugins/mwm-ai")
    args = parser.parse_args()
    try:
        validate(args.plugin)
        print("Claude directory allowlists passed: manifest, loaded MCP configs, and package.json files")
    except (ValueError, OSError) as error:
        print(f"Claude directory validation failed: {error}", file=sys.stderr)
        sys.exit(1)
