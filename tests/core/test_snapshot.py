import unittest

from blumcl.core.snapshot import (
    Snapshot,
    SnapshotFile,
    compare_snapshots,
)


class TestSnapshotFile(unittest.TestCase):

    def test_crear_archivo(self):
        archivo = SnapshotFile(
            path="/tmp/test.txt",
            size_bytes=100,
        )

        self.assertEqual(
            archivo.path,
            "/tmp/test.txt",
        )

        self.assertEqual(
            archivo.size_bytes,
            100,
        )

        self.assertIsNone(
            archivo.sha256,
        )

    def test_no_acepta_tamano_negativo(self):
        with self.assertRaises(ValueError):
            SnapshotFile(
                path="/tmp/test.txt",
                size_bytes=-1,
            )

    def test_hash_valido(self):
        archivo = SnapshotFile(
            path="/tmp/test.txt",
            size_bytes=100,
            sha256="a" * 64,
        )

        self.assertEqual(
            archivo.sha256,
            "a" * 64,
        )


class TestSnapshot(unittest.TestCase):

    def test_crear_snapshot(self):
        snapshot = Snapshot.create(
            sequence=1,
            total_bytes=1000,
            used_bytes=600,
            free_bytes=400,
        )

        self.assertEqual(
            snapshot.snapshot_id,
            "BLUMCL-S-000001",
        )

        self.assertEqual(
            snapshot.total_bytes,
            1000,
        )

        self.assertEqual(
            snapshot.used_bytes,
            600,
        )

        self.assertEqual(
            snapshot.free_bytes,
            400,
        )

    def test_agregar_archivo(self):
        snapshot = Snapshot.create(
            sequence=2,
        )

        snapshot.add_file(
            path="/tmp/a.txt",
            size_bytes=500,
        )

        self.assertEqual(
            len(snapshot.files),
            1,
        )

        self.assertEqual(
            snapshot.files[0].path,
            "/tmp/a.txt",
        )

    def test_serializacion_json(self):
        snapshot = Snapshot.create(
            sequence=3,
            used_bytes=5000,
        )

        snapshot.add_file(
            path="/tmp/documento.pdf",
            size_bytes=2500,
        )

        payload = snapshot.to_json()

        restaurado = Snapshot.from_json(
            payload
        )

        self.assertEqual(
            restaurado.snapshot_id,
            snapshot.snapshot_id,
        )

        self.assertEqual(
            restaurado.used_bytes,
            5000,
        )

        self.assertEqual(
            len(restaurado.files),
            1,
        )

        self.assertEqual(
            restaurado.files[0].path,
            "/tmp/documento.pdf",
        )

    def test_indice_de_archivos(self):
        snapshot = Snapshot.create(
            sequence=4,
        )

        snapshot.add_file(
            "/tmp/a.txt",
            100,
        )

        snapshot.add_file(
            "/tmp/b.txt",
            200,
        )

        indice = snapshot.file_index()

        self.assertEqual(
            len(indice),
            2,
        )

        self.assertEqual(
            indice["/tmp/a.txt"].size_bytes,
            100,
        )


class TestCompareSnapshots(unittest.TestCase):

    def test_detecta_archivo_nuevo(self):
        anterior = Snapshot.create(
            sequence=1,
        )

        actual = Snapshot.create(
            sequence=2,
        )

        actual.add_file(
            "/tmp/nuevo.txt",
            100,
        )

        cambios = compare_snapshots(
            anterior,
            actual,
        )

        self.assertEqual(
            len(cambios.added),
            1,
        )

        self.assertEqual(
            cambios.added[0].path,
            "/tmp/nuevo.txt",
        )

    def test_detecta_archivo_eliminado(self):
        anterior = Snapshot.create(
            sequence=1,
        )

        anterior.add_file(
            "/tmp/eliminado.txt",
            100,
        )

        actual = Snapshot.create(
            sequence=2,
        )

        cambios = compare_snapshots(
            anterior,
            actual,
        )

        self.assertEqual(
            len(cambios.removed),
            1,
        )

        self.assertEqual(
            cambios.removed[0].path,
            "/tmp/eliminado.txt",
        )

    def test_detecta_crecimiento(self):
        anterior = Snapshot.create(
            sequence=1,
        )

        anterior.add_file(
            "/tmp/proyecto.dat",
            100,
        )

        actual = Snapshot.create(
            sequence=2,
        )

        actual.add_file(
            "/tmp/proyecto.dat",
            500,
        )

        cambios = compare_snapshots(
            anterior,
            actual,
        )

        self.assertEqual(
            len(cambios.grew),
            1,
        )

        archivo, delta = cambios.grew[0]

        self.assertEqual(
            archivo.path,
            "/tmp/proyecto.dat",
        )

        self.assertEqual(
            delta,
            400,
        )

    def test_detecta_reduccion(self):
        anterior = Snapshot.create(
            sequence=1,
        )

        anterior.add_file(
            "/tmp/proyecto.dat",
            500,
        )

        actual = Snapshot.create(
            sequence=2,
        )

        actual.add_file(
            "/tmp/proyecto.dat",
            200,
        )

        cambios = compare_snapshots(
            anterior,
            actual,
        )

        self.assertEqual(
            len(cambios.shrank),
            1,
        )

        archivo, delta = cambios.shrank[0]

        self.assertEqual(
            archivo.path,
            "/tmp/proyecto.dat",
        )

        self.assertEqual(
            delta,
            -300,
        )

    def test_detecta_sin_cambios(self):
        anterior = Snapshot.create(
            sequence=1,
        )

        anterior.add_file(
            "/tmp/igual.txt",
            100,
        )

        actual = Snapshot.create(
            sequence=2,
        )

        actual.add_file(
            "/tmp/igual.txt",
            100,
        )

        cambios = compare_snapshots(
            anterior,
            actual,
        )

        self.assertEqual(
            len(cambios.unchanged),
            1,
        )

        self.assertEqual(
            cambios.changed_count,
            0,
        )

    def test_no_modifica_snapshots(self):
        anterior = Snapshot.create(
            sequence=1,
        )

        anterior.add_file(
            "/tmp/a.txt",
            100,
        )

        actual = Snapshot.create(
            sequence=2,
        )

        actual.add_file(
            "/tmp/a.txt",
            200,
        )

        anterior_json = anterior.to_json()
        actual_json = actual.to_json()

        compare_snapshots(
            anterior,
            actual,
        )

        self.assertEqual(
            anterior.to_json(),
            anterior_json,
        )

        self.assertEqual(
            actual.to_json(),
            actual_json,
        )


if __name__ == "__main__":
    unittest.main()
