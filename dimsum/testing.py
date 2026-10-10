"""testing.py - pengujian global memakai library unittest."""
import os
import tempfile
import unittest
from dimsum.models import MenuItem, Pesanan
from dimsum.validasi import DataTidakValid, validasi_angka_positif
from dimsum import fileio, processing


class TestDimsum(unittest.TestCase):
    def setUp(self):
        """Dijalankan sebelum tiap test: siapkan folder sementara & data."""
        self.tmp = tempfile.TemporaryDirectory()
        self.menu_path = os.path.join(self.tmp.name, "menu.txt")
        fileio.buat_file_menu(self.menu_path)
        self.menu = fileio.baca_menu(self.menu_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_validasi_angka_valid(self):
        self.assertEqual(validasi_angka_positif("5"), 5)

    def test_validasi_angka_negatif_raise(self):
        with self.assertRaises(DataTidakValid):
            validasi_angka_positif("-2")

    def test_validasi_bukan_angka_raise(self):
        with self.assertRaises(DataTidakValid):
            validasi_angka_positif("abc")

    def test_subtotal(self):
        p = Pesanan(1, "Zaki", self.menu["HG01"], 3)
        self.assertEqual(p.hitung_subtotal(), 54000)

    def test_hitung_total_args(self):
        self.assertEqual(processing.hitung_total(10, 20, 30), 60)

    def test_file_menu_x_tidak_menimpa(self):
        self.assertFalse(fileio.buat_file_menu(self.menu_path))  # sudah ada

    def test_simpan_dan_baca_pesanan_lewati_baris_rusak(self):
        path = os.path.join(self.tmp.name, "pesanan.txt")
        fileio.simpan_pesanan(Pesanan(1, "Zaki", self.menu["HG01"], 2), path)
        with open(path, "a", encoding="utf-8") as f:
            f.write("baris;rusak\n")                      # sengaja rusak
        fileio.simpan_pesanan(Pesanan(2, "Dewi", self.menu["SM02"], 1), path)
        hasil = fileio.baca_pesanan(path, self.menu)
        self.assertEqual(len(hasil), 2)                   # rusak dilewati

    def test_menu_terlaris(self):
        daftar = [Pesanan(1, "A", self.menu["HG01"], 2),
                  Pesanan(2, "B", self.menu["SM02"], 5)]
        self.assertEqual(processing.menu_terlaris(daftar, n=1)[0][0],
                         "Siomay Ayam")

    def test_file_pesanan_tidak_ada(self):
        self.assertEqual(
            fileio.baca_pesanan(os.path.join(self.tmp.name, "x.txt"), self.menu), [])


if __name__ == "__main__":
    unittest.main()
