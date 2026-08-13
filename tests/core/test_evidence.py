import json
import tempfile
import unittest
from pathlib import Path

from blumcl.core.evidence import (
    Evidence,
    EvidenceAction,
    EvidenceCategory,
    EvidenceSource,
    EvidenceReason,
    calculate_sha256,
    evidence_from_file,
)


class TestEvidence(unittest.TestCase):

    def test_create_evidence(self):
        evidence = Evidence.create(
            sequence=42,
            path="/tmp/example.zip",
            source=EvidenceSource.STORAGE_SCANNER,
            category=EvidenceCategory.REVIEW,
            size_bytes=1_400_000_000,
            file_type="zip",
            confidence=0.87,
        )

        self.assertEqual(
            evidence.evidence_id,
            "BLUMCL-E-000042",
        )

        self.assertEqual(
            evidence.path,
            "/tmp/example.zip",
        )

        self.assertEqual(
            evidence.size_bytes,
            1_400_000_000,
        )

        self.assertEqual(
            evidence.category,
            EvidenceCategory.REVIEW,
        )

        self.assertEqual(
            evidence.action,
            EvidenceAction.NONE,
        )

    def test_add_reason(self):
        evidence = Evidence.create(
            sequence=1,
            path="/tmp/example.zip",
            source=EvidenceSource.STORAGE_SCANNER,
        )

        evidence.add_reason(
            "large_file",
            "Archivo de gran tamaño.",
        )

        self.assertTrue(evidence.has_reasons())

        self.assertEqual(
            len(evidence.reasons),
            1,
        )

        self.assertEqual(
            evidence.reasons[0].code,
            "large_file",
        )

    def test_json_serialization(self):
        evidence = Evidence.create(
            sequence=10,
            path="/tmp/example.zip",
            source=EvidenceSource.STORAGE_SCANNER,
            confidence=0.90,
        )

        evidence.add_reason(
            "large_file",
            "Archivo grande.",
        )

        payload = json.loads(
            evidence.to_json()
        )

        self.assertEqual(
            payload["evidence_id"],
            "BLUMCL-E-000010",
        )

        self.assertEqual(
            payload["confidence"],
            0.90,
        )

        self.assertEqual(
            payload["reasons"][0]["code"],
            "large_file",
        )

    def test_invalid_confidence(self):
        with self.assertRaises(ValueError):
            Evidence.create(
                sequence=1,
                path="/tmp/example.zip",
                source=EvidenceSource.STORAGE_SCANNER,
                confidence=1.5,
            )

    def test_invalid_evidence_id(self):
        with self.assertRaises(ValueError):
            Evidence(
                evidence_id="INVALID-001",
                timestamp=Evidence.now(),
                path="/tmp/example.zip",
            )

    def test_sha256(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.txt"

            path.write_text(
                "BLUMCL",
                encoding="utf-8",
            )

            digest = calculate_sha256(path)

            self.assertEqual(
                len(digest),
                64,
            )

            evidence = evidence_from_file(
                sequence=100,
                path=path,
                source=EvidenceSource.STORAGE_SCANNER,
                calculate_hash=True,
            )

            self.assertEqual(
                evidence.sha256,
                digest,
            )

            self.assertEqual(
                evidence.size_bytes,
                6,
            )

    def test_file_observation_does_not_modify_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protected.txt"

            original = "BLUMCL evidence test"

            path.write_text(
                original,
                encoding="utf-8",
            )

            evidence_from_file(
                sequence=200,
                path=path,
                source=EvidenceSource.STORAGE_SCANNER,
            )

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                original,
            )


if __name__ == "__main__":
    unittest.main()
