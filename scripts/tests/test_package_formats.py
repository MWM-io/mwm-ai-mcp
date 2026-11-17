import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_script("build-plugin-zip")
CLAUDE = load_script("check-claude-package")
EXPECTED_AUTH = {"type": "oauth", "client": {"mode": "dcr"}, "baseScopes": ["mcp:access", "offline_access"]}


class ClaudeDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="mwm-claude-fields-")
        self.addCleanup(self.temporary.cleanup)
        self.plugin = Path(self.temporary.name) / "plugin"
        shutil.copytree(ROOT / "plugins/mwm-ai", self.plugin)

    def test_native_source_accepts_isolated_openai_configuration(self):
        CLAUDE.validate(self.plugin)
        codex = json.loads((self.plugin / ".mcp.codex.json").read_text())
        self.assertIn("extensions", codex["mcpServers"]["mwm-ai"])

    def test_claude_source_rejects_each_previously_shared_openai_field(self):
        path = self.plugin / ".mcp.json"
        original = json.loads(path.read_text())
        for key, value in (("http_headers", {}), ("tool_timeout_sec", 900), ("extensions", {})):
            with self.subTest(key=key):
                config = json.loads(json.dumps(original))
                config["mcpServers"]["mwm-ai"][key] = value
                path.write_text(json.dumps(config))
                with self.assertRaisesRegex(ValueError, key):
                    CLAUDE.validate(self.plugin)

    def test_unknown_oauth_field_is_refused(self):
        path = self.plugin / ".mcp.json"
        config = json.loads(path.read_text())
        config["mcpServers"]["mwm-ai"]["oauth"] = {"clientSecret": "not-a-credential"}
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "clientSecret"):
            CLAUDE.validate(self.plugin)

    def test_non_runtime_manifest_metadata_is_refused(self):
        path = self.plugin / ".claude-plugin/plugin.json"
        manifest = json.loads(path.read_text())
        manifest["privacyPolicyUrl"] = "https://example.invalid/privacy"
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "privacyPolicyUrl"):
            CLAUDE.validate(self.plugin)

    def test_package_json_requires_plain_object_and_allowed_fields(self):
        path = self.plugin / "package.json"
        for invalid in ([], "package text", {"name": "mwm-ai", "scripts": {}}, {"engines": {"node": {"version": "20"}}}):
            with self.subTest(value=invalid):
                path.write_text(json.dumps(invalid))
                with self.assertRaises(ValueError):
                    CLAUDE.validate(self.plugin)
        path.write_text(json.dumps({"name": "mwm-ai", "license": "MIT", "engines": {"node": ">=20"}}))
        CLAUDE.validate(self.plugin)

    def test_explicit_mcp_reference_cannot_load_openai_fields(self):
        path = self.plugin / ".claude-plugin/plugin.json"
        manifest = json.loads(path.read_text())
        manifest["mcpServers"] = "./.mcp.codex.json"
        path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            CLAUDE.validate(self.plugin)


class DistributionFormatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = BUILDER.validate()

    def test_claude_zip_uses_exact_validated_source_without_openai_files(self):
        payload = BUILDER.package_payload(self.manifest, "claude")
        self.assertEqual(payload[".mcp.json"], (ROOT / "plugins/mwm-ai/.mcp.json").read_bytes())
        self.assertNotIn(".mcp.codex.json", payload)
        self.assertNotIn("mcp.json", payload)
        self.assertFalse(any(path.startswith(".codex-plugin/") for path in payload))
        CLAUDE.validate_mcp(json.loads(payload[".mcp.json"]), "Claude ZIP")

    def test_desktop_zip_resolves_codex_config_with_auth_timeout_and_header(self):
        payload = BUILDER.package_payload(self.manifest, "desktop")
        codex = json.loads(payload[".codex-plugin/plugin.json"])
        server = json.loads(payload[codex["mcpServers"].removeprefix("./")])["mcpServers"]["mwm-ai"]
        self.assertEqual(server["extensions"]["com.openai"]["auth"], EXPECTED_AUTH)
        self.assertEqual(server["tool_timeout_sec"], 900)
        self.assertEqual(server["http_headers"], {"X-MWM-Plugin-Version": self.manifest["version"]})
        self.assertIn("interface", codex)
        self.assertEqual(codex["extensions"]["com.openai"]["onboardingSkill"], "./skills/setup/SKILL.md")

    def test_submission_zip_preserves_portable_oauth_and_openai_metadata(self):
        payload = BUILDER.package_payload(self.manifest, "submission")
        manifest = json.loads(payload["plugin.json"])
        config = json.loads(payload["mcp.json"])
        server = config["mcpServers"]["mwm-ai"]
        self.assertEqual(server["type"], "streamable-http")
        self.assertEqual(server["url"], "https://mcp.mwm.ai/mcp")
        self.assertEqual(server["extensions"]["com.openai"]["auth"], EXPECTED_AUTH)
        self.assertEqual(config["$schema"], "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json")
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"], self.manifest["interface"])
        self.assertEqual(manifest["extensions"]["com.openai"]["review"], self.manifest["extensions"]["com.openai"]["review"])
        setup = manifest["extensions"]["com.openai"]["onboardingSkill"].removeprefix("./")
        self.assertIn(setup, payload)
        self.assertNotIn(".mcp.json", payload)
        self.assertNotIn(".mcp.codex.json", payload)
        self.assertFalse(any(path.startswith((".codex-plugin/", ".claude-plugin/")) for path in payload))


if __name__ == "__main__":
    unittest.main()
