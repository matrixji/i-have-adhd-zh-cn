"""Check failures that could break distribution or upstream migration."""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_repo


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for path in check_repo.REQUIRED:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        for directory in ("skills", "docs", "evals"):
            for path in (ROOT / directory).rglob("*.md"):
                if "results" in path.parts:
                    continue
                target = self.root / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)

    def test_distribution_is_self_contained(self):
        self.assertEqual([], check_repo.check(self.root))

    def test_missing_license_is_rejected(self):
        (self.root / check_repo.SKILL.parent / "LICENSE").unlink()
        self.assertTrue(any("LICENSE" in e for e in check_repo.check(self.root)))

    def test_changed_license_is_rejected(self):
        (self.root / check_repo.SKILL.parent / "LICENSE").write_text("different license")
        self.assertTrue(any("license must match" in e for e in check_repo.check(self.root)))

    def test_broken_document_link_is_rejected(self):
        with (self.root / "README.md").open("a") as stream:
            stream.write("\n[missing](docs/missing.md)\n")
        self.assertTrue(any("broken local link" in e for e in check_repo.check(self.root)))

    def test_link_outside_distribution_is_rejected(self):
        with (self.root / "README.md").open("a") as stream:
            stream.write("\n[external](../private.md)\n")
        self.assertTrue(any("leaves repository" in e for e in check_repo.check(self.root)))

    def test_short_source_sha_is_rejected(self):
        path = self.root / "docs/upstream.json"
        data = json.loads(path.read_text())
        data["sources"]["upstream"]["reviewed_commit"] = "1ecea19"
        path.write_text(json.dumps(data))
        self.assertTrue(any("full reviewed commit" in e for e in check_repo.check(self.root)))

    def test_duplicate_case_is_rejected(self):
        path = self.root / "evals/cases.jsonl"
        first = path.read_text().splitlines()[0]
        with path.open("a") as stream:
            stream.write(first + "\n")
        self.assertTrue(any("Duplicate case id" in e for e in check_repo.check(self.root)))

    def test_invalid_criteria_is_rejected(self):
        path = self.root / "evals/cases.jsonl"
        case = json.loads(path.read_text().splitlines()[0])
        case["criteria"] = [123]
        path.write_text(json.dumps(case) + "\n")
        self.assertTrue(any("criteria must contain" in e for e in check_repo.check(self.root)))

    def test_unexpected_public_skill_is_rejected(self):
        other = self.root / "skills/other/SKILL.md"
        other.parent.mkdir()
        other.write_text("another skill")
        self.assertTrue(any("one public skill" in e for e in check_repo.check(self.root)))

    def test_returning_plugin_adapter_is_rejected(self):
        path = self.root / ".claude-plugin/plugin.json"
        path.parent.mkdir()
        path.write_text("{}")
        self.assertTrue(any("host adapters" in e for e in check_repo.check(self.root)))


if __name__ == "__main__":
    unittest.main()
