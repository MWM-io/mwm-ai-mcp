#!/usr/bin/env python3
"""Validate and package MWM AI, including dotfiles and excluding local files."""

import argparse
import importlib.util
import json
import sys
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins/mwm-ai"
FILES = (
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/icon.png",
    ".mcp.json",
    "README.md",
    "LICENSE",
)
SHARED_MANIFEST_FIELDS = (
    "name", "version", "description", "author", "homepage", "repository",
    "license", "privacyPolicyUrl", "keywords", "skills", "mcpServers",
)
DIRECTORIES = ("skills", "commands", "assets")
# The one header a package may carry: the plugin version, non-secret, read by
# the server for telemetry and the alias window. `headers` is Claude Code's
# key, `http_headers` Codex's; neither changes the URL, so the OAuth resource
# (RFC 9728 audience) stays https://mcp.mwm.ai/mcp.
VERSION_HEADER = "X-MWM-Plugin-Version"


def read_json(relative):
    return json.loads((PLUGIN / relative).read_text())


def package_path(relative):
    path = (PLUGIN / relative).resolve()
    if not relative.startswith("./") or not path.is_relative_to(PLUGIN.resolve()):
        raise ValueError(f"Path must stay inside the plugin: {relative}")
    if not path.exists():
        raise ValueError(f"Missing packaged path: {relative}")
    return path


def check_headers(name, config, version, allowed):
    for key in ("headers", "http_headers", "env_http_headers", "headersHelper", "http_headers_helper"):
        value = config.get(key)
        if value is None:
            continue
        if not allowed or key not in ("headers", "http_headers"):
            raise ValueError(f"Do not package connection credentials in headers ({name}.{key})")
        if value != {VERSION_HEADER: version}:
            raise ValueError(f"{name}.{key} may only carry {VERSION_HEADER}: {version}")


def lint_skills():
    """Run scripts/check-skills.py; any error refuses the build."""
    spec = importlib.util.spec_from_file_location("check_skills", REPO / "scripts/check-skills.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    errors = module.check()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        raise ValueError(f"check-skills found {len(errors)} error(s)")


def validate():
    lint_skills()
    manifest = read_json(FILES[0])
    claude = read_json(FILES[1])
    for field in SHARED_MANIFEST_FIELDS:
        if manifest.get(field) != claude.get(field):
            raise ValueError(f"Codex and Claude manifests differ on {field}")
    if "interface" in claude or "extensions" in claude:
        raise ValueError("Claude manifest must not contain OpenAI-only metadata")
    if (PLUGIN / "LICENSE").read_bytes() != (REPO / "LICENSE").read_bytes():
        raise ValueError("Package and repository licenses differ")
    for field in ("skills", "mcpServers"):
        package_path(manifest[field])
    interface = manifest["interface"]
    for field in ("composerIcon", "logo"):
        package_path(interface[field])
    for relative in interface.get("screenshots", []):
        package_path(relative)
    setup = package_path(manifest["extensions"]["com.openai"]["onboardingSkill"])
    if not setup.is_file() or setup.name != "SKILL.md":
        raise ValueError("Onboarding must point to a packaged SKILL.md")

    desktop = read_json(".mcp.json")["mcpServers"]
    submission = read_json("mcp.json")
    if submission["$schema"] != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
        raise ValueError("Missing Agent Plugins MCP schema declaration")
    if desktop.keys() != submission["mcpServers"].keys():
        raise ValueError("Desktop and submission MCP servers differ")
    for name, server in desktop.items():
        remote = submission["mcpServers"][name]
        if server["type"] != "http" or remote["type"] != "streamable-http":
            raise ValueError(f"Unexpected transport for {name}")
        if server["url"] != remote["url"] or server["url"] != "https://mcp.mwm.ai/mcp":
            raise ValueError(f"MCP production endpoints differ for {name}")
        auth = server["extensions"]["com.openai"]["auth"]
        if auth != remote["extensions"]["com.openai"]["auth"]:
            raise ValueError(f"OAuth declarations differ for {name}")
        if auth["type"] != "oauth" or auth["client"] != {"mode": "dcr"}:
            raise ValueError(f"Expected public OAuth client registration for {name}")
        check_headers(name, server, manifest["version"], allowed=True)
        check_headers(name, remote, manifest["version"], allowed=False)
        if server.get("headers") != server.get("http_headers"):
            raise ValueError(f"{name}: headers and http_headers must declare the same version")
        scopes = auth["baseScopes"]
        if not scopes or any(not scope.strip() for scope in scopes):
            raise ValueError(f"Missing OAuth scopes for {name}")
    return manifest


def submission_manifest(manifest):
    portable = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        **{key: manifest[key] for key in (
            "name", "version", "description", "author", "homepage",
            "repository", "license", "keywords",
        )},
    }
    portable["extensions"] = {
        "com.openai": {
            **manifest["extensions"]["com.openai"],
            "interface": manifest["interface"],
        },
    }
    return portable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format", choices=("desktop", "claude", "submission"), default="desktop",
        help="Desktop, native Claude, or portable OpenAI submission package",
    )
    parser.add_argument("--output", type=Path, help="Destination ZIP (defaults to dist/)")
    args = parser.parse_args()
    manifest = validate()
    version = manifest["version"]
    suffix = f"-{args.format}" if args.format != "desktop" else ""
    output = args.output or REPO / f"dist/mwm-ai-plugin{suffix}-{version}.zip"
    if args.format == "desktop":
        paths = [PLUGIN / relative for relative in FILES]
    elif args.format == "claude":
        paths = [PLUGIN / relative for relative in FILES if not relative.startswith(".codex-plugin/")]
    else:
        paths = [PLUGIN / "README.md", PLUGIN / "LICENSE"]
    for directory in DIRECTORIES:
        paths.extend(
            path for path in (PLUGIN / directory).rglob("*")
            if path.is_file() and path.name != ".DS_Store"
            and not path.name.startswith("._") and path.suffix != ".zip"
            and "__pycache__" not in path.parts
        )
    if output.resolve() in [path.resolve() for path in paths]:
        raise ValueError("ZIP destination cannot replace a packaged source file")
    payload = {path.relative_to(PLUGIN).as_posix(): path.read_bytes() for path in paths}
    if args.format == "claude":
        native = {"mcpServers": {
            name: {key: server[key] for key in ("type", "url", "headers")}
            for name, server in read_json(".mcp.json")["mcpServers"].items()
        }}
        payload[".mcp.json"] = (json.dumps(native, indent=2) + "\n").encode()
    if args.format == "submission":
        payload["plugin.json"] = (json.dumps(submission_manifest(manifest), indent=2, ensure_ascii=False) + "\n").encode()
        payload["mcp.json"] = (PLUGIN / "mcp.json").read_bytes()
    declared_setup = manifest["extensions"]["com.openai"]["onboardingSkill"].removeprefix("./")
    if declared_setup not in payload:
        raise ValueError("Declared onboarding skill is excluded from the ZIP")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, data in sorted(payload.items()):
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    print(f"Built MWM AI {version} ({args.format}): {output.resolve()} ({len(payload)} files)")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, OSError) as error:
        print(f"Package error: {error}", file=sys.stderr)
        sys.exit(1)
