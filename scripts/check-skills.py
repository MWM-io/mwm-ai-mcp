#!/usr/bin/env python3
"""Lint the MWM AI skills, commands, agents/openai.yaml files and READMEs.

Skills are domain packs: judgment, not facts. Store rules, limits, states and
how MWM behaves come from the server (its results and its knowledge base,
read with get_publishing_knowledge); tool choice comes from the tool
descriptions; consent, budget and rights are the server's rails. The lint
refuses what belongs elsewhere:

1. tool names (from scripts/tool-names.json, the server's tools/list), except
   get_publishing_knowledge in the Facts section; setup may name it anywhere;
2. call sequences ("first ... then", "call X with Y");
3. parameter, enum and reason-code recipes (dry_run, consent_token, locked...);
4. restated rails (consent tokens, budgets, the right to publish...);
5. digits, except "iOS 27" and "iOS 18": numbers come from the knowledge base;
6. "Not available here" lists;
7. plugin or server version clauses;
8. unknown or replaced topic ids (checked against scripts/kb-index.json);
9. length and the required sections of a pack.

Commands, each agents/openai.yaml and the skills follow rules 1 to 8. The
READMEs are for people and carry versions and URLs: there, a tool name must
be registered, a topic id known, a skills/ path real, and every pack listed.

Run it alone (python3 scripts/check-skills.py) or through
scripts/build-plugin-zip.py, which refuses to build when it finds an error.
"""

import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins/mwm-ai"
SKILLS = PLUGIN / "skills"
COMMANDS = PLUGIN / "commands"
READMES = (REPO / "README.md", PLUGIN / "README.md")

PACKS = (
    "working-with-mwm", "store-copy", "store-visuals", "brand-visuals", "acquisition-pages",
    "privacy-and-legal", "app-privacy", "shipping", "live-moments", "reviews",
    "market-research", "app-analytics", "setup",
)
# The one pack that may name tools: it connects the plugin and checks it with
# a free read of the knowledge base (spec K6, §5.4.11).
TOOL_EXEMPT = {"setup"}
KNOWLEDGE_TOOL = "get_publishing_knowledge"

SECTIONS = (
    "When this applies",
    "The job and what good looks like",
    "How a pro decides",
    "Do",
    "Don't",
    "Pitfalls",
    "Store facts",
)
FACTS_SECTION = SECTIONS[-1]
FACTS_PARAGRAPH = (
    "Tool results carry the store rules and limits they depend on, each with its "
    "source and the date it was checked. `get_publishing_knowledge` answers "
    "questions on this skill's topics the same way (topics: {topics}). When you "
    "use one of these facts, give its source and date."
)
DESCRIPTION_WORDS = (40, 80)
BODY_WORDS = (350, 500)
DIGIT_WHITELIST = ("iOS 27", "iOS 18")

WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SNAKE = re.compile(r"(?<![\w$])[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?![\w])")
DOTTED = re.compile(r"\b(?:guidance|presentation|consent|result|results|interface)\.[a-z_]+", re.I)
TOPIC_SECTIONS = ("app-store", "google-play", "cross-store", "aso", "mwm")
# Taxonomies of earlier designs that the knowledge base replaced.
REPLACED_SECTIONS = ("stores", "store-copy", "shipping", "store-visuals")
TOPIC = re.compile(
    r"(?<![\w/.-])((?:%s)/[a-z0-9-]+)(#[a-z0-9-]+)?(?![\w/-]|\.\w)"
    % "|".join(map(re.escape, TOPIC_SECTIONS + REPLACED_SECTIONS))
)
LINK = re.compile(r"\]\(([^)\s]+)\)")

# Rule 2: an order of calls is the server's to give, in its guidance.
SEQUENCES = (
    (r"\bfirst\b[^.!?;:\n]*\bthen\b", "a 'first ... then' sequence"),
    (r"\bcall(?:s|ed|ing)?\s+(?:it|them|this|that|the\s+\w+|`?[\w.]+`?)\s+with\b", "a 'call X with Y' recipe"),
    (r"\b(?:then|next|afterwards?|before|after|once done)\s*,?\s+call(?:s|ing)?\b", "a call sequence"),
    (r"\bcall(?:s|ed|ing)?\s+`", "a call to a named tool"),
    (r"\bstep\s+(?:one|two|three|four|five)\b", "numbered steps"),
)
# Rule 3: parameter names, enum values and reason codes.
PARAMETERS = (
    "dry_run", "dry run", "consent_token", "cost_token", "cost token", "plan_hash",
    "review_hash", "draft_hash", "if_match", "approval", "user_words",
    "reason_code", "reason code", "locked", "version_string", "handoff_id",
    "override_of", "idempotency", "enum", "enums", "parameter", "parameters",
)
# Rule 4: consent, budget and rights are enforced and explained by the server.
RAILS = (
    (r"\bconsent tokens?\b", "consent tokens"),
    (r"\bsingle-use\b", "a single-use rail"),
    (r"\bone-time tokens?\b", "a one-time token"),
    (r"\bfree (?:count|allowance|quota)\b", "the free budget"),
    (r"\b(?:daily|assistant) (?:budget|allowance|limit|cap|quota)\b", "the budget"),
    (r"\bper day\b|\ba day freely\b", "the budget"),
    (r"\bright to publish\b", "publishing rights"),
    (r"\bthe server (?:enforces|checks|refuses|rejects|blocks|requires|guards)\b", "what the server enforces"),
    (r"\bwhat the server enforces\b", "what the server enforces"),
    (r"\b(?:is|are|gets|get) refused\b", "a server refusal"),
    (r"\breceipts?\b", "write receipts"),
    (r"\bunder (?:direct|confirm)\b", "assistant setting values"),
    (r"\bstore[ _-](?:send|publish)\b", "assistant setting names"),
    (r"\b(?:publish|send) setting\b", "assistant setting names"),
)
# Rule 6.
UNAVAILABLE = (
    r"\bnot available (?:here|in mwm|through mwm|with mwm)\b",
    r"\bnot supported (?:here|by mwm|in mwm)\b",
    r"\bunavailable here\b",
    r"^#+\s*not available\b",
    r"\bmwm (?:cannot|can't|does not|doesn't) (?:do|support|offer)\b",
)
# Rule 7.
VERSIONS = (
    r"\b(?:plugin|server|skills?|mcp) versions?\b",
    r"\bversions? of (?:the|this) (?:plugin|server|skills?)\b",
    r"\b(?:older|newer|earlier|later|previous|current) (?:plugins?|servers?|clients?|skills?)\b",
    r"\bserver of\b",
    r"\bsince (?:the )?(?:plugin|server)\b",
)
# Rule 9: a pack works with MWM's tools without ranking them above anything
# else (OpenAI review, 9 November 2026: Fair play, Respect user intent). It never
# puts MWM above the model's knowledge, another skill, the platform's
# instructions or another plugin, never rules out other tools and hides none.
STEERING = (
    (r"\b(?:mwm|the server|the result|a result) is right\b", "MWM ranked above the rest"),
    (r"\byour (?:memory|knowledge|training)\b|\bwhat you remember\b|\bfrom memory\b", "the model's knowledge belittled"),
    (r"\bfrom general knowledge\b|\bnever from\b", "the model's knowledge belittled"),
    (r"\bno substitute\b|\b(?:do not|don't|never) (?:try|use|call) (?:any )?other\b", "other tools ruled out"),
    (r"\b(?:other|another) (?:tools?|plugins?|connectors?|(?:image )?generators?)\b", "other tools ruled out"),
    (r"\binstead of (?:your|the model|other|another)\b", "other sources ruled out"),
    (r"\b(?:ignore|override)s? (?:the |any |previous |older |other )*(?:instructions?|skills?|system)\b", "instructions overridden"),
    (r"\bolder instructions?\b|\bnever name (?:the )?tools\b", "instructions overridden or tools hidden"),
    (r"\blawyers? (?:reviewed|approved)\b", "a promotional claim"),
)


class Linter:
    def __init__(self):
        self.errors = []
        self.tools = set(json.loads((REPO / "scripts/tool-names.json").read_text()))
        index = json.loads((REPO / "scripts/kb-index.json").read_text())
        self.topics = {topic["id"] for topic in index["topics"]}
        self.facts = {fact["id"] for topic in index["topics"] for fact in topic.get("facts", [])}
        self.verbs = {name.split("_", 1)[0] for name in self.tools}

    def error(self, path, line, message):
        self.errors.append(f"{path.relative_to(REPO)}:{line}: {message}")

    # Rules 1 to 8 over a run of text that starts at `line` in `path`.
    def text(self, path, line, text, allow_tools=(), allow_backticks=False):
        for offset, row in enumerate(text.split("\n")):
            at = line + offset
            stripped = row
            for allowed in DIGIT_WHITELIST:
                stripped = stripped.replace(allowed, "")
            if re.search(r"\d", stripped):
                self.error(path, at, f"digit in {row.strip()!r}: numbers come from MWM's knowledge base")
            for name in SNAKE.findall(row):
                if name in allow_tools:
                    continue
                if name in self.tools:
                    self.error(path, at, f"tool name {name}: tool choice belongs to the tool descriptions")
                else:
                    self.error(path, at, f"parameter or enum {name}: the server's results carry them")
            for match in DOTTED.findall(row):
                self.error(path, at, f"result field {match}: the server's results carry it")
            if "`" in row and not allow_backticks:
                self.error(path, at, "code span: a pack names no tool, parameter or value")
            lowered = row.lower()
            for word in PARAMETERS:
                if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(word), lowered):
                    self.error(path, at, f"parameter recipe word {word!r}")
            for pattern, what in SEQUENCES:
                if re.search(pattern, row, re.I):
                    self.error(path, at, f"{what}: the server's guidance orders calls")
            for pattern, what in RAILS:
                if re.search(pattern, row, re.I):
                    self.error(path, at, f"restated rail ({what}): the server enforces and explains it")
            for pattern in UNAVAILABLE:
                if re.search(pattern, row, re.I):
                    self.error(path, at, "'not available' list: describe_capabilities answers it")
            for pattern in VERSIONS:
                if re.search(pattern, row, re.I):
                    self.error(path, at, "plugin or server version clause")
            for pattern, what in STEERING:
                if re.search(pattern, row, re.I):
                    self.error(path, at, f"steering ({what}): a pack never ranks MWM above the model, a skill, the platform or another plugin")
            self.topic_ids(path, at, row)

    def topic_ids(self, path, line, row):
        for topic, fact in TOPIC.findall(row):
            if topic.split("/", 1)[0] in REPLACED_SECTIONS:
                self.error(path, line, f"replaced topic id {topic}")
            elif topic not in self.topics:
                self.error(path, line, f"unknown topic id {topic}")
            elif fact and topic + fact not in self.facts:
                self.error(path, line, f"unknown fact id {topic}{fact}")

    def links(self, path, line, text):
        for offset, row in enumerate(text.split("\n")):
            for target in LINK.findall(row):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                if not (path.parent / target.split("#", 1)[0]).exists():
                    self.error(path, line + offset, f"link to a missing file: {target}")

    @staticmethod
    def frontmatter(path):
        content = path.read_text()
        if not content.startswith("---\n"):
            raise ValueError("no frontmatter")
        end = content.index("\n---\n", 4)
        fields = {}
        for row in content[4:end].split("\n"):
            key, _, value = row.partition(":")
            value = value.strip()
            fields[key.strip()] = json.loads(value) if value.startswith('"') else value
        body_line = content[: end + 5].count("\n") + 1
        return fields, content[end + 5:], body_line

    def skill(self, directory):
        name = directory.name
        path = directory / "SKILL.md"
        if not path.is_file():
            self.error(directory, 0, "missing SKILL.md")
            return
        for item in directory.rglob("*"):
            relative = item.relative_to(directory).as_posix()
            if item.is_file() and relative not in ("SKILL.md", "agents/openai.yaml") and item.name != ".DS_Store":
                self.error(item, 0, "a pack holds only SKILL.md and agents/openai.yaml (no references/)")
        try:
            fields, body, body_line = self.frontmatter(path)
        except ValueError as error:
            self.error(path, 1, str(error))
            return
        if fields.get("name") != name:
            self.error(path, 2, f"name must be {name!r}")
        description = fields.get("description", "")
        allow = {KNOWLEDGE_TOOL} if name in TOOL_EXEMPT else set()
        self.text(path, 3, description, allow_tools=allow)
        count = len(WORD.findall(description))
        if not DESCRIPTION_WORDS[0] <= count <= DESCRIPTION_WORDS[1]:
            self.error(path, 3, f"description has {count} words, wants {DESCRIPTION_WORDS[0]} to {DESCRIPTION_WORDS[1]}")
        marker = "Use when the person says things like"
        if marker not in description:
            self.error(path, 3, f"description lacks {marker!r}")
        elif len(re.findall(r'"[^"]+"', description.split(marker, 1)[1])) < 3:
            self.error(path, 3, "description wants at least three quoted phrases after its 'Use when'")
        boundary = re.search(r"\bNot for\b(.*)", description)
        targets = re.findall(r"\(([a-z-]+)\)", boundary.group(1)) if boundary else []
        if not targets:
            self.error(path, 3, "description lacks a 'Not for ... (<pack>)' boundary")
        for target in targets:
            if target not in PACKS or target == name:
                self.error(path, 3, f"boundary names {target!r}, not another pack")

        lines = body.split("\n")
        titles = [(i, row) for i, row in enumerate(lines) if row.startswith("# ")]
        if len(titles) != 1:
            self.error(path, body_line, "a pack has exactly one '# ' title")
        headings = [(i, row[3:].strip()) for i, row in enumerate(lines) if row.startswith("## ")]
        if [heading for _, heading in headings] != list(SECTIONS):
            self.error(path, body_line, f"sections must be exactly: {', '.join(SECTIONS)}")
        if any(row.startswith("###") for row in lines):
            self.error(path, body_line, "no sub-sections in a pack")
        facts_at = next((i for i, heading in headings if heading == FACTS_SECTION), len(lines))
        before = "\n".join(lines[:facts_at])
        self.text(path, body_line, before, allow_tools=allow, allow_backticks=name in TOOL_EXEMPT)
        self.links(path, body_line, body)
        words = len(WORD.findall("\n".join(row for row in lines[:facts_at] if not row.startswith("#"))))
        if not BODY_WORDS[0] <= words <= BODY_WORDS[1]:
            self.error(path, body_line, f"body has {words} words before its Facts section, wants {BODY_WORDS[0]} to {BODY_WORDS[1]}")
        facts = "\n".join(lines[facts_at + 1:]).strip()
        topics = re.search(r"\(topics: (.+?)\)\.", facts)
        cited = re.findall(r"`([^`]+)`", topics.group(1)) if topics else []
        if not cited or facts != FACTS_PARAGRAPH.format(topics=", ".join(f"`{t}`" for t in cited)):
            self.error(path, body_line + facts_at, "the Facts section must be the fixed paragraph with the pack's topic ids")
        for topic in cited:
            if topic not in self.topics:
                self.error(path, body_line + facts_at, f"unknown topic id {topic}")
        if len(set(cited)) != len(cited):
            self.error(path, body_line + facts_at, "a topic id is cited twice")
        self.yaml(directory / "agents/openai.yaml", name)

    def yaml(self, path, name):
        if not path.is_file():
            self.error(path, 0, "missing agents/openai.yaml")
            return
        found = set()
        allow = {KNOWLEDGE_TOOL} if name in TOOL_EXEMPT else set()
        for number, row in enumerate(path.read_text().split("\n"), 1):
            match = re.match(r'^\s*(display_name|short_description|default_prompt|description):\s*(.*)$', row)
            if not match:
                continue
            key, value = match.groups()
            found.add(key)
            value = json.loads(value) if value.startswith('"') else value
            self.text(path, number, value.replace(f"${name}", ""), allow_tools=allow)
        for key in ("display_name", "short_description", "default_prompt"):
            if key not in found:
                self.error(path, 0, f"missing interface.{key}")

    def command(self, path):
        try:
            fields, body, body_line = self.frontmatter(path)
        except ValueError as error:
            self.error(path, 1, str(error))
            return
        if not fields.get("description"):
            self.error(path, 2, "a command needs a description")
        for number, key in enumerate(fields, 2):
            self.text(path, number, str(fields[key]))
        self.text(path, body_line, body.replace("$ARGUMENTS", ""))
        self.links(path, body_line, body)

    def readme(self, path):
        content = path.read_text()
        for number, row in enumerate(content.split("\n"), 1):
            for name in SNAKE.findall(row):
                if name.split("_", 1)[0] in self.verbs and name not in self.tools:
                    self.error(path, number, f"{name} looks like a tool the server does not register")
            self.topic_ids(path, number, row)
            for skill in re.findall(r"skills/([a-z0-9-]+)", row):
                if skill not in PACKS:
                    self.error(path, number, f"skills/{skill} is not a pack")
        self.links(path, 1, content)
        if path.parent == PLUGIN:
            for pack in PACKS:
                if f"`skills/{pack}/`" not in content:
                    self.error(path, 0, f"the contents table lacks skills/{pack}/")
            if "| Old name | Pack |" not in content:
                self.error(path, 0, "the README lacks the old name to pack table")

    def run(self):
        present = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
        for missing in sorted(set(PACKS) - set(present)):
            self.error(SKILLS, 0, f"missing pack {missing}")
        for extra in sorted(set(present) - set(PACKS)):
            self.error(SKILLS / extra, 0, "not one of the packs")
        for name in present:
            self.skill(SKILLS / name)
        for path in sorted(COMMANDS.glob("*.md")):
            self.command(path)
        for path in READMES:
            self.readme(path)
        return self.errors


def check():
    """Return the lint's errors, an empty list when every file passes."""
    return Linter().run()


def main():
    errors = check()
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"check-skills: {len(errors)} error(s)", file=sys.stderr)
        sys.exit(1)
    print(f"check-skills: {len(PACKS)} packs, commands, agents and READMEs pass")


if __name__ == "__main__":
    main()
