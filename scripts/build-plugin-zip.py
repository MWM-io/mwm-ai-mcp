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
    ".mcp.codex.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/icon.png",
    ".mcp.json",
    "README.md",
    "LICENSE",
)
SHARED_MANIFEST_FIELDS = (
    "name", "version", "description", "author", "homepage", "repository",
    "license", "keywords", "skills",
)
DIRECTORIES = ("skills", "commands", "assets")
# The one header a package may carry: the plugin version, non-secret, read by
# the server for telemetry and the alias window. Each host has its own config:
# `headers` is Claude Code's key, `http_headers` Codex's. Neither changes the URL, so the OAuth resource
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
        if key not in allowed:
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
    claude = read_json(".claude-plugin/plugin.json")
    spec = importlib.util.spec_from_file_location("check_claude", REPO / "scripts/check-claude-package.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    checker.validate(PLUGIN)
    for field in SHARED_MANIFEST_FIELDS:
        if manifest.get(field) != claude.get(field):
            raise ValueError(f"Codex and Claude manifests differ on {field}")
    if (PLUGIN / "LICENSE").read_bytes() != (REPO / "LICENSE").read_bytes():
        raise ValueError("Package and repository licenses differ")
    for host in (manifest, claude):
        for field in ("skills", "mcpServers"):
            package_path(host[field])
    if manifest["mcpServers"] != "./.mcp.codex.json" or claude["mcpServers"] != "./.mcp.json":
        raise ValueError("Claude and Codex must reference their separate MCP configurations")
    interface = manifest["interface"]
    for field in ("composerIcon", "logo"):
        package_path(interface[field])
    for relative in interface.get("screenshots", []):
        package_path(relative)
    setup = package_path(manifest["extensions"]["com.openai"]["onboardingSkill"])
    if not setup.is_file() or setup.name != "SKILL.md":
        raise ValueError("Onboarding must point to a packaged SKILL.md")

    desktop = read_json(".mcp.codex.json")["mcpServers"]
    native = read_json(".mcp.json")["mcpServers"]
    if desktop.keys() != native.keys():
        raise ValueError("Claude and Codex MCP servers differ")
    for name, server in desktop.items():
        remote = native[name]
        if server["type"] != "http" or remote["type"] != "http":
            raise ValueError(f"Unexpected transport for {name}")
        if server["url"] != remote["url"] or server["url"] != "https://mcp.mwm.ai/mcp":
            raise ValueError(f"MCP production endpoints differ for {name}")
        auth = server["extensions"]["com.openai"]["auth"]
        if auth["type"] != "oauth" or auth["client"] != {"mode": "dcr"}:
            raise ValueError(f"Expected public OAuth client registration for {name}")
        check_headers(name, server, manifest["version"], allowed={"http_headers"})
        check_headers(name, remote, manifest["version"], allowed={"headers"})
        expected_header = {VERSION_HEADER: manifest["version"]}
        if server.get("http_headers") != expected_header or remote.get("headers") != expected_header:
            raise ValueError(f"{name}: each host must declare the current plugin version")
        if server["tool_timeout_sec"] != 900:
            raise ValueError(f"{name}: preserve Codex's long-running tool timeout")
        scopes = auth["baseScopes"]
        if not scopes or any(not scope.strip() for scope in scopes):
            raise ValueError(f"Missing OAuth scopes for {name}")
    return manifest


def submission_mcp():
    """Generate the portable root file without exposing it to Claude's loader."""
    desktop = read_json(".mcp.codex.json")["mcpServers"]
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {
            name: {"type": "streamable-http", "url": server["url"], "extensions": server["extensions"]}
            for name, server in desktop.items()
        },
    }


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


def package_payload(manifest, package_format):
    if package_format == "desktop":
        paths = [PLUGIN / relative for relative in FILES]
    elif package_format == "claude":
        paths = [PLUGIN / relative for relative in FILES
                 if not relative.startswith(".codex-plugin/") and relative != ".mcp.codex.json"]
    else:
        paths = [PLUGIN / "README.md", PLUGIN / "LICENSE"]
    for directory in DIRECTORIES:
        paths.extend(
            path for path in (PLUGIN / directory).rglob("*")
            if path.is_file() and path.name != ".DS_Store"
            and not path.name.startswith("._") and path.suffix != ".zip"
            and "__pycache__" not in path.parts
        )
    payload = {path.relative_to(PLUGIN).as_posix(): path.read_bytes() for path in paths}
    if package_format == "submission":
        payload["plugin.json"] = (json.dumps(submission_manifest(manifest), indent=2, ensure_ascii=False) + "\n").encode()
        payload["mcp.json"] = (json.dumps(submission_mcp(), indent=2) + "\n").encode()
    declared_setup = manifest["extensions"]["com.openai"]["onboardingSkill"].removeprefix("./")
    if declared_setup not in payload:
        raise ValueError("Declared onboarding skill is excluded from the ZIP")
    return payload


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
    payload = package_payload(manifest, args.format)
    if output.resolve().is_relative_to(PLUGIN.resolve()):
        raise ValueError("ZIP destination must stay outside the plugin source directory")
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
