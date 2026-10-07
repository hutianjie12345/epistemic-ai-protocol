#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline publication checks, not a model evaluation or a security guarantee."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

IGNORED = {'.git', '__pycache__', '.venv'}
PRIVATE_DIRS = {'private', '_local', 'review-notes'}
DENIED_SUFFIXES = {'.zip', '.sqlite', '.sqlite3', '.db', '.pem', '.key', '.p12', '.pfx'}
# Findings omit matched values so reports do not echo possible credentials.
PATTERNS = {
    'private_document_link': re.compile(r'https?://(?:docs\.google\.com/(?:document|spreadsheets|presentation)/d/|drive\.google\.com/(?:file/d/|drive/folders/))', re.I),
    'private_user_path': re.compile(r'(?:[A-Z]:[\\/]Users[\\/]|/(?:Users|home)/[A-Za-z0-9_.-]+/)', re.I),
    'email_address': re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    'github_token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b'),
    'key_like_value': re.compile(r'\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}\b'),
    'aws_access_key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'private_key_block': re.compile(r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----'),
}
INLINE_LINK = re.compile(r'!?\[[^\]\n]*\]\(([^)\n]+)\)')
FENCES = re.compile(r'^\s*(`{3,}|~{3,})')


def without_code_fences(text: str) -> str:
    lines: list[str] = []
    marker: str | None = None
    for line in text.splitlines():
        match = FENCES.match(line)
        if match:
            char = match.group(1)[0]
            if marker is None:
                marker = char
            elif marker == char:
                marker = None
            lines.append('')
        else:
            lines.append(line if marker is None else '')
    return '\n'.join(lines)


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[dict] = []
    counts = {'files_scanned': 0, 'markdown_files': 0, 'relative_links_checked': 0,
              'snapshots_checked': 0, 'workflow_files_checked': 0}

    def fail(rule: str, path: str, line: int | None = None) -> None:
        item = {'rule': rule, 'path': path}
        if line is not None:
            item['line'] = line
        errors.append(item)

    texts: dict[str, str] = {}
    if not root.is_dir():
        fail('repository_missing', '.')
        return {'ok': False, 'counts': counts, 'errors': errors}
    for p in sorted(root.rglob('*')):
        rel = p.relative_to(root)
        if any(part in IGNORED for part in rel.parts):
            continue
        if p.is_symlink():
            fail('symlink_not_reviewed', rel.as_posix())
            continue
        if not p.is_file():
            continue
        name = rel.as_posix()
        counts['files_scanned'] += 1
        if any(part in PRIVATE_DIRS for part in rel.parts) or p.name.startswith('.env') or p.suffix.lower() in DENIED_SUFFIXES:
            fail('private_or_archive_file', name)
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            fail('unreadable_or_binary_file', name)
            continue
        texts[name] = text
        for rule, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                fail(rule, name, text[:match.start()].count('\n') + 1)

    for name in ('README.md', 'LICENSE', 'LICENSE-CODE', 'CHANGELOG.md', 'snapshots.json'):
        if name not in texts:
            fail('required_file_missing', name)
    try:
        manifest = json.loads(texts.get('snapshots.json', '{}'))
        snapshots = manifest['snapshots']
        if manifest.get('schema_version') != 1 or not isinstance(snapshots, list) or not snapshots:
            raise ValueError('invalid manifest')
        registered: set[str] = set()
        for item in snapshots:
            name = item['path']
            if not isinstance(name, str) or name in registered or not name.startswith('prompt/'):
                raise ValueError('invalid snapshot path')
            registered.add(name)
            path = root / name
            if not path.resolve().is_relative_to(root) or path.is_symlink():
                fail('snapshot_path_outside_repository', name)
                continue
            if name not in texts:
                fail('snapshot_missing', name)
                continue
            counts['snapshots_checked'] += 1
            if not re.fullmatch(r'[0-9a-f]{64}', item['sha256']) or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                fail('snapshot_hash_mismatch', name)
            if texts[name].splitlines()[0] != '# ' + item['title']:
                fail('snapshot_title_mismatch', name)
            if item['version_label'] not in item['title']:
                fail('snapshot_version_mismatch', name)
            if not item.get('source_kind'):
                fail('snapshot_source_missing', name)
        if manifest.get('selected_snapshot') not in registered:
            fail('selected_snapshot_unregistered', 'snapshots.json')
        for name in texts:
            if name.startswith('prompt/') and name.endswith('.md') and name not in registered:
                fail('unregistered_snapshot', name)
    except (ValueError, KeyError, TypeError, IndexError, OSError):
        fail('invalid_manifest', 'snapshots.json')

    for name, text in texts.items():
        if not name.endswith('.md'):
            continue
        counts['markdown_files'] += 1
        for match in INLINE_LINK.finditer(without_code_fences(text)):
            raw = match.group(1).strip()
            target = raw[1:raw.index('>')] if raw.startswith('<') and '>' in raw else raw.split()[0]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            local = unquote(parsed.path)
            path = root / local.lstrip('/') if local.startswith('/') else (root / name).parent / local
            counts['relative_links_checked'] += 1
            if not path.resolve().is_relative_to(root) or not path.is_file():
                fail('broken_or_escaping_local_link', name)

    workflows = [n for n in texts if n.startswith('.github/workflows/') and n.endswith(('.yml', '.yaml'))]
    if not workflows:
        fail('workflow_missing', '.github/workflows')
    for name in workflows:
        text = texts[name]
        counts['workflow_files_checked'] += 1
        if re.search(r'pull_request_target|workflow_run|self-hosted|\$\{\{\s*secrets\.', text):
            fail('unsafe_workflow_surface', name)
        if not re.search(r'^permissions:\s*\n\s+contents: read\s*$', text, re.M) or re.search(r':\s*write\b|write-all', text):
            fail('workflow_permissions', name)
        if 'runs-on: ubuntu-24.04' not in text or 'persist-credentials: false' not in text:
            fail('workflow_checkout_or_runner', name)
        actions = re.findall(r'uses:\s*(\S+)', text)
        if not actions or any(not re.fullmatch(r'actions/checkout@[0-9a-f]{40}', a) for a in actions):
            fail('workflow_unreviewed_dependency', name)
    return {'ok': not errors, 'counts': counts, 'errors': errors,
            'scope': 'Offline artifact checks only; not model evaluation, authorization, or comprehensive secret scanning.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true', help='Print a machine-readable report')
    args = parser.parse_args()
    result = validate(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('PASS' if result['ok'] else 'FAIL')
        print(json.dumps(result['counts'], ensure_ascii=False))
        for error in result['errors']:
            print(json.dumps(error, ensure_ascii=False))
        print(result['scope'])
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
