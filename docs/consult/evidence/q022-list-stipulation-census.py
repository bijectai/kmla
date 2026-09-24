#!/usr/bin/env python3
"""Read-only source census for Q-022; not grounding or a representation fix."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from harness.case_reader import read_case
from harness.facts import STIP_SIGNATURES
from harness.runtime import sha256

signatures = set(STIP_SIGNATURES.values())
paths = sorted((ROOT / 'human/sara/sara/cases').glob('*.pl'))
rows = []
for path in paths:
    case = read_case(path)
    for index, clause in enumerate(case.clauses, 1):
        head = clause.head
        if head.tag != 'compound' or (head.value, len(head.args)) not in signatures:
            continue
        list_positions = [i for i, arg in enumerate(head.args, 1)
                          if any(n.tag == 'list' for n in arg.walk())]
        if not list_positions:
            continue
        rows.append({
            'case': path.name, 'source_sha256': case.source.sha256,
            'source_clause_index_1based': index, 'kind': clause.kind,
            'signature': f'{head.value}/{len(head.args)}',
            'list_argument_positions': list_positions,
            'clause_verbatim': case.original_text(clause.ast),
            'list_nodes': [{'text': case.original_text(n),
                            'element_tags': [a.tag for a in n.args],
                            'variable_names': [a.value.name for a in n.walk() if a.tag == 'var']}
                           for arg in head.args for n in arg.walk() if n.tag == 'list'],
        })
assert len(paths) == 376
print(json.dumps({
    'scope': 'syntactic supplied-head census only; not runtime solution completeness',
    'original_case_count': len(paths),
    'list_head_clause_count': len(rows),
    'distinct_case_count': len({row['case'] for row in rows}),
    'rows': rows,
    'reader_sha256': sha256(ROOT / 'harness/case_reader.py'),
    'script_sha256': sha256(Path(__file__)),
}, indent=2))
