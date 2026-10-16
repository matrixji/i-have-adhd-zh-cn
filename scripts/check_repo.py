#!/usr/bin/env python3
"""Offline contracts for the standalone simplified Chinese skill."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import run_evals
import run_scenario_eval

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/i-have-adhd-zh-cn/SKILL.md")
SOURCES = {
    "upstream": "https://github.com/ayghri/i-have-adhd.git",
    "reference-zh-tw": "https://github.com/panda850819/i-have-adhd-zh-tw.git",
}
REQUIRED = (
    SKILL, SKILL.parent / "LICENSE", SKILL.parent / "agents/openai.yaml",
    Path("LICENSE"), Path("logo.png"), Path("README.md"), Path("INSTALL.md"),
    Path("AGENTS.md"), Path("CONTRIBUTING.md"), Path("docs/upstream.json"),
    Path("docs/upstream.md"), Path("evals/cases.jsonl"), Path("evals/rubric.md"),
    Path("evals/README.md"), Path(".github/workflows/validate.yml"),
    Path("evals/scenarios/persistence-topic-switch-stop/case.jsonl"),
)


def check_frontmatter(path: Path) -> list[str]:
    """Check the deliberately flat metadata used by the public skill."""
    match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    if not match:
        return [f"{path}: missing frontmatter"]
    metadata = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(":")
        if not separator or key in metadata:
            return [f"{path}: invalid or duplicate metadata field"]
        metadata[key] = value.strip().strip("\"'")
    errors = []
    if metadata.get("name") != path.parent.name:
        errors.append(f"{path}: skill name must match its directory")
    if not 1 <= len(metadata.get("description", "")) <= 1024:
        errors.append(f"{path}: description must contain 1 to 1024 characters")
    if metadata.get("license") != "MIT":
        errors.append(f"{path}: MIT license must be declared")
    return errors


def check_sources(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["docs/upstream.json: expected an object"]
    errors = []
    if data.get("schema_version") != 1:
        errors.append("docs/upstream.json: unsupported schema_version")
    local = data.get("local", {})
    if not isinstance(local, dict) or local.get("skill_path") != SKILL.as_posix():
        errors.append("docs/upstream.json: incorrect local skill path")
    sources = data.get("sources")
    if not isinstance(sources, dict) or set(sources) != set(SOURCES):
        return errors + ["docs/upstream.json: both source repositories are required"]
    for name, expected_url in SOURCES.items():
        source = sources[name]
        if not isinstance(source, dict):
            errors.append(f"docs/upstream.json: {name} must be an object")
            continue
        if source.get("url") != expected_url:
            errors.append(f"docs/upstream.json: incorrect {name} source URL")
        if not re.fullmatch(r"[0-9a-f]{40}", str(source.get("reviewed_commit", ""))):
            errors.append(f"docs/upstream.json: {name} needs a full reviewed commit SHA")
        if not source.get("branch") or not source.get("skill_path"):
            errors.append(f"docs/upstream.json: {name} needs branch and skill_path")
    return errors


def check_local_links(root: Path, path: Path) -> list[str]:
    errors = []
    for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", path.read_text(encoding="utf-8")):
        target = unquote(target.split("#", 1)[0])
        if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(root.resolve()):
            errors.append(f"{path.relative_to(root)}: link leaves repository: {target}")
        elif not resolved.exists():
            errors.append(f"{path.relative_to(root)}: broken local link: {target}")
    return errors


def check(root: Path = ROOT) -> list[str]:
    missing = [f"Missing file: {path}" for path in REQUIRED if not (root / path).is_file()]
    if missing:
        return missing
    errors = check_frontmatter(root / SKILL)
    if sorted(path.relative_to(root) for path in (root / "skills").glob("*/SKILL.md")) != [SKILL]:
        errors.append("Exactly one public skill is expected")
    if (root / "LICENSE").read_bytes() != (root / SKILL.parent / "LICENSE").read_bytes():
        errors.append("Skill license must match the root license")
    if "Copyright (c) 2026 Ayoub Ghriss" not in (root / "LICENSE").read_text():
        errors.append("Original copyright notice is missing")
    try:
        errors.extend(check_sources(root / "docs/upstream.json"))
        cases = run_evals.load_cases(root / "evals/cases.jsonl")
        errors.extend(run_evals.validate_cases(cases))
        for case in cases:
            for field in ("category", "prompt"):
                if not isinstance(case.get(field), str) or not case[field].strip():
                    errors.append(f"Case {case.get('id')}: {field} must be non-empty text")
            criteria = case.get("criteria")
            if not isinstance(criteria, list) or any(
                not isinstance(item, str) or not item.strip() for item in criteria
            ):
                errors.append(f"Case {case.get('id')}: criteria must contain non-empty strings")
        run_scenario_eval.load_scenario(root / "evals/scenarios/persistence-topic-switch-stop")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(f"Invalid source or evaluation data: {exc}")
    docs = list(root.glob("*.md"))
    for directory in ("skills", "docs", "evals"):
        docs.extend(path for path in (root / directory).rglob("*.md") if "results" not in path.parts)
    for path in docs:
        errors.extend(check_local_links(root, path))
    for directory in (".claude-plugin", ".codex-plugin", ".cursor", "hooks", "extensions", ".opencode"):
        if any(path.is_file() for path in (root / directory).rglob("*")):
            errors.append(f"Standalone skill must not include host adapters: {directory}")
    if (root / ".git").exists():
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", ".agents/skills"], cwd=root,
            capture_output=True, text=True, check=True, timeout=10,
        ).stdout
        if tracked:
            errors.append("Local maintenance skills must not be tracked")
    return errors


if __name__ == "__main__":
    findings = check()
    for finding in findings:
        print(f"ERROR: {finding}", file=sys.stderr)
    if findings:
        raise SystemExit(1)
    print("Repository contracts passed (offline; no model behavior evaluated).")
