# SPDX-License-Identifier: MIT
"""Synthetic failure fixtures test the checker, not a language model."""
from __future__ import annotations
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from check_repository import validate

ROOT = Path(__file__).resolve().parents[1]

class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'fixture'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '.git', '.venv'))

    def append(self, rel, content):
        p = self.root / rel
        p.write_text(p.read_text(encoding='utf-8') + '\n' + content + '\n', encoding='utf-8')

    def assertRule(self, rule):
        result = validate(self.root)
        self.assertFalse(result['ok'])
        self.assertIn(rule, [e['rule'] for e in result['errors']], result)

    def test_clean_repository(self):
        result = validate(self.root)
        self.assertTrue(result['ok'], result)

    def test_prompt_byte_change(self):
        self.append('prompt/v2.9.md', 'Changed without a new snapshot.')
        self.assertRule('snapshot_hash_mismatch')

    def test_missing_license(self):
        (self.root / 'LICENSE').unlink()
        self.assertRule('required_file_missing')

    def test_broken_markdown_link(self):
        self.append('README.md', '[example](does-not-exist.md)')
        self.assertRule('broken_or_escaping_local_link')

    def test_private_document_link(self):
        self.append('README.md', 'https://' + 'docs.google.com/' + 'document/d/' + 'SYNTHETIC_TEST_ONLY')
        self.assertRule('private_document_link')

    def test_synthetic_key_no_echo(self):
        key = 'ghp' + '_' + 'A' * 36
        self.append('README.md', key)
        result = validate(self.root)
        self.assertIn('github_token', [e['rule'] for e in result['errors']])
        self.assertNotIn(key, json.dumps(result))

    def test_local_user_path(self):
        self.append('README.md', 'C:' + '/' + 'Users/' + 'Example/private.txt')
        self.assertRule('private_user_path')

    def test_unregistered_snapshot(self):
        (self.root / 'prompt/v99.md').write_text('# Synthetic fixture\n', encoding='utf-8')
        self.assertRule('unregistered_snapshot')

    def test_unreviewed_workflow_pin(self):
        p = self.root / '.github/workflows/validate.yml'
        p.write_text(p.read_text().replace('11d5960a326750d5838078e36cf38b85af677262', 'v4'))
        self.assertRule('workflow_unreviewed_dependency')

    def test_write_permission(self):
        p = self.root / '.github/workflows/validate.yml'
        p.write_text(p.read_text().replace('contents: read', 'contents: write'))
        self.assertRule('workflow_permissions')

    def test_private_directory(self):
        p = self.root / 'private'
        p.mkdir()
        (p / 'note.md').write_text('Synthetic unpublished note.\n')
        self.assertRule('private_or_archive_file')

    def test_manifest_path_escape(self):
        p = self.root / 'snapshots.json'
        data = json.loads(p.read_text())
        data['snapshots'][0]['path'] = 'prompt/../../outside.md'
        p.write_text(json.dumps(data))
        self.assertRule('snapshot_path_outside_repository')

if __name__ == '__main__':
    unittest.main()
