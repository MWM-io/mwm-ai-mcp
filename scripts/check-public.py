#!/usr/bin/env python3
"""Verify an exported public tree, its inventory, documentation, and packages."""

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


REPO = Path(__file__).resolve().parents[1]
INVENTORY = ".release-manifest.json"
IGNORED = {".git", "dist", "__pycache__"}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(rb'"private_key"\s*:\s*"[^"\s]'),
)


def main():
    inventory = json.loads((REPO / INVENTORY).read_text())
    if inventory["repository"] != "MWM-io/mwm-ai-mcp":
        raise ValueError("Unexpected public repository")
    expected = set(inventory["files"]) | {INVENTORY}
    # In a checkout, local IDE/cache files ignored by Git are not published.
    # Export snapshots without .git still validate every file strictly.
    visible = None
    if (REPO / ".git").exists():
        visible = set(subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=REPO,
        ).decode().split("\0"))
    actual = set()
    for path in REPO.rglob("*"):
        relative = path.relative_to(REPO)
        if any(part in IGNORED for part in relative.parts):
            continue
        if visible is not None and relative.as_posix() not in visible:
            continue
        if path.is_symlink():
            raise ValueError(f"Public symlink: {relative}")
        if path.is_file():
            actual.add(relative.as_posix())
    if actual != expected:
        raise ValueError(f"Inventory mismatch: missing={sorted(expected - actual)}, unexpected={sorted(actual - expected)}")
    for name, digest in inventory["files"].items():
        relative = PurePosixPath(name)
        if relative.is_absolute() or relative.as_posix() != name or any(part in (".", "..", ".git") for part in relative.parts):
            raise ValueError(f"Unsafe inventory path: {name}")
        if any(part in ("review", "private", "internal", ".env", ".idea") for part in relative.parts):
            raise ValueError(f"Private path in public inventory: {name}")
        data = (REPO / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"Content hash differs from release inventory: {name}")
        if any(pattern.search(data) for pattern in SECRET_PATTERNS):
            raise ValueError(f"Possible credential in public file: {name}")
        if name.endswith(".json"):
            json.loads(data)
        if name.endswith(".md"):
            check_document(REPO / name, data.decode())
    spec = importlib.util.spec_from_file_location("build_plugin", REPO / "scripts/build-plugin-zip.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    manifest = builder.validate()
    if (manifest["version"] != inventory["version"] or manifest["license"] != "MIT"
            or manifest["repository"] != "https://github.com/MWM-io/mwm-ai-mcp"):
        raise ValueError("Public manifest version, license, or repository mismatch")
    claude = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    codex = json.loads((REPO / ".agents/plugins/marketplace.json").read_text())
    if claude["name"] != codex["name"] or claude["name"] != "mwm":
        raise ValueError("Marketplace names differ")
    if (claude["plugins"][0]["name"] != manifest["name"]
            or codex["plugins"][0]["name"] != manifest["name"]
            or claude["plugins"][0]["source"] != "./plugins/mwm-ai"
            or codex["plugins"][0]["source"] != {"source": "local", "path": "./plugins/mwm-ai"}):
        raise ValueError("Marketplace plugin names or source paths differ")
    print(f"Public validation passed: {len(actual)} files, MWM AI {manifest['version']}, links, configs, skills, and inventory")
    print("Credential patterns are a packaging check, not a complete secret audit.")


def check_document(path, content):
    for block in re.findall(r"```json\s*\n(.*?)\n```", content, re.S):
        json.loads(block)
    links = re.findall(r"\]\(([^\s)]+)\)", content)
    links += re.findall(r'(?:href|src)="([^"]+)"', content)
    for link in links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (path.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(REPO) or not target.exists():
            raise ValueError(f"Broken local documentation link in {path.relative_to(REPO)}: {link}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, ValueError, OSError) as error:
        print(f"Public validation failed: {error}", file=sys.stderr)
        sys.exit(1)
