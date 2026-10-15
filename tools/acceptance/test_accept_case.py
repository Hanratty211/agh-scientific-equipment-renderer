"""Portable contract tests; no session logs or Blender installation required."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from accept_case import run, validate


class AcceptanceContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.scene = self.root / 'fixture.blend'
        # Unit fixture only: not presented as a real Blender scene.
        self.scene.write_bytes(b'synthetic scene identity for contract validation')
        self.audit = self.root / 'audit.py'
        self.audit.write_text('# synthetic auditor identity\n')
        self.contract = self.root / 'contract.json'
        self.expected = ['fixture.component', 'fixture.connection']
        self.contract.write_text(json.dumps({
            'audit_script': 'audit.py',
            'audit_sha256': hashlib.sha256(self.audit.read_bytes()).hexdigest(),
            'expected_check_ids': self.expected,
            'scope': 'synthetic unit fixture',
        }))
        self.report = {
            'scene': str(self.scene.resolve()),
            'sha256': hashlib.sha256(self.scene.read_bytes()).hexdigest(),
            'checks': [{'id': name, 'status': 'PASS'} for name in self.expected],
            'counts': {'PASS': 2, 'FAIL': 0},
        }

    def test_valid_report(self):
        self.assertEqual(validate(self.report, self.scene, self.expected), [])

    def test_wrong_case_coverage(self):
        self.assertTrue(validate(self.report, self.scene, ['other.component', 'other.connection']))

    def test_duplicate_and_missing_checks(self):
        for checks in [[], self.report['checks'][:1], [self.report['checks'][0]] * 2]:
            with self.subTest(checks=checks):
                report = copy.deepcopy(self.report)
                report['checks'] = checks
                self.assertTrue(validate(report, self.scene, self.expected))

    def test_failed_check_and_forged_counts(self):
        failed = copy.deepcopy(self.report)
        failed['checks'][0]['status'] = 'FAIL'
        self.assertTrue(validate(failed, self.scene, self.expected))
        self.report['counts']['PASS'] = 0
        self.assertTrue(validate(self.report, self.scene, self.expected))

    def test_wrong_scene_identity(self):
        for key, value in [('sha256', '0' * 64), ('scene', 'other.blend')]:
            with self.subTest(key=key):
                report = copy.deepcopy(self.report)
                report[key] = value
                self.assertTrue(validate(report, self.scene, self.expected))

    def test_malformed_report(self):
        for report in [None, [], {}, {'checks': [None]}, {'checks': [{'id': []}]}]:
            with self.subTest(report=report):
                self.assertTrue(validate(report, self.scene, self.expected))

    def test_existing_output_is_immutable(self):
        out = self.root / 'existing'
        out.mkdir()
        original = out / 'execution.log'
        original.write_text('prior failure must survive')
        with self.assertRaises(FileExistsError):
            run(self.scene, out, self.contract, 'not-executed', 1)
        self.assertEqual(original.read_text(), 'prior failure must survive')

    def test_missing_scene_records_failure(self):
        out = self.root / 'missing-run'
        result = run(self.root / 'missing.blend', out, self.contract, 'not-executed', 1)
        self.assertEqual(result['status'], 'FAIL')
        self.assertFalse(result['audit_started'])
        self.assertEqual(json.loads((out / 'gate.json').read_text())['status'], 'FAIL')

    def test_startup_error_records_failure(self):
        out = self.root / 'startup-error'
        result = run(self.scene, out, self.contract, str(self.root / 'missing-blender'), 1)
        self.assertEqual(result['status'], 'FAIL')
        self.assertEqual(result['exit_code'], 127)
        self.assertEqual(result['scene_sha256_before'], result['scene_sha256_after'])

    def test_modified_auditor_rejected(self):
        self.audit.write_text('# changed auditor\n')
        with self.assertRaisesRegex(ValueError, 'Frozen auditor hash mismatch'):
            run(self.scene, self.root / 'tampered', self.contract, 'not-executed', 1)
        self.assertFalse((self.root / 'tampered').exists())


if __name__ == '__main__':
    unittest.main()
