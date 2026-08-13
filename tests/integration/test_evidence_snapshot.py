import unittest

from blumcl.core.evidence import (
    Evidence,
    EvidenceCategory,
    EvidenceSource,
)

from blumcl.core.snapshot import Snapshot


class TestEvidenceSnapshotIntegration(unittest.TestCase):

    def test_evidence_queda_asociada_al_snapshot(self):
        snapshot = Snapshot.create(
            sequence=100,
            total_bytes=10_000,
            used_bytes=6_000,
            free_bytes=4_000,
        )

        evidence = Evidence.create(
            sequence=1,
            path="/tmp/ejemplo.zip",
            source=EvidenceSource.STORAGE_SCANNER,
            category=EvidenceCategory.REVIEW,
            size_bytes=1_000,
            snapshot_id=snapshot.snapshot_id,
        )

        evidence.add_reason(
            "large_file",
            "Archivo de prueba para integración.",
        )

        snapshot.add_evidence(evidence)

        self.assertEqual(
            len(snapshot.evidences),
            1,
        )

        self.assertEqual(
            snapshot.evidences[0].evidence_id,
            "BLUMCL-E-000001",
        )

        self.assertEqual(
            snapshot.evidences[0].snapshot_id,
            snapshot.snapshot_id,
        )

    def test_snapshot_conserva_evidencia_al_serializar(self):
        snapshot = Snapshot.create(
            sequence=101,
        )

        evidence = Evidence.create(
            sequence=2,
            path="/tmp/documento.pdf",
            source=EvidenceSource.STORAGE_SCANNER,
            category=EvidenceCategory.REVIEW,
            size_bytes=500,
            snapshot_id=snapshot.snapshot_id,
        )

        evidence.add_reason(
            "review",
            "Debe revisarse.",
        )

        snapshot.add_evidence(evidence)

        payload = snapshot.to_json()

        restored = Snapshot.from_json(
            payload
        )

        self.assertEqual(
            len(restored.evidences),
            1,
        )

        restored_evidence = restored.evidences[0]

        self.assertEqual(
            restored_evidence.evidence_id,
            "BLUMCL-E-000002",
        )

        self.assertEqual(
            restored_evidence.path,
            "/tmp/documento.pdf",
        )

        self.assertEqual(
            restored_evidence.snapshot_id,
            restored.snapshot_id,
        )

        self.assertEqual(
            len(restored_evidence.reasons),
            1,
        )

    def test_no_permite_evidencia_de_otro_snapshot(self):
        snapshot_a = Snapshot.create(
            sequence=102,
        )

        snapshot_b = Snapshot.create(
            sequence=103,
        )

        evidence = Evidence.create(
            sequence=3,
            path="/tmp/otro.txt",
            source=EvidenceSource.STORAGE_SCANNER,
            snapshot_id=snapshot_a.snapshot_id,
        )

        with self.assertRaises(ValueError):
            snapshot_b.add_evidence(evidence)


if __name__ == "__main__":
    unittest.main()
