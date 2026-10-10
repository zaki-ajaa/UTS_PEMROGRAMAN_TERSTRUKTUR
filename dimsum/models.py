"""models.py - dua class: MenuItem dan Pesanan."""
from dimsum.validasi import validasi_tidak_kosong, validasi_angka_positif


class MenuItem:
    """Satu item menu dimsum. **atribut menampung field tambahan (kategori, dll)."""

    def __init__(self, kode, nama, harga, **atribut):
        self.kode = validasi_tidak_kosong(kode, "kode")
        self.nama = validasi_tidak_kosong(nama, "nama")
        self.harga = validasi_angka_positif(harga, "harga")
        self.atribut = atribut            # contoh: {"kategori": "Kukus"}

    def to_line(self):
        """Ubah objek menjadi satu baris teks untuk disimpan ke file."""
        return f"{self.kode};{self.nama};{self.harga};{self.atribut.get('kategori', '-')}"


class Pesanan:
    """Satu pesanan pelanggan."""

    def __init__(self, id_pesanan, pelanggan, menu, jumlah):
        self.id = id_pesanan
        self.pelanggan = validasi_tidak_kosong(pelanggan, "pelanggan")
        self.menu = menu                  # objek MenuItem
        self.jumlah = validasi_angka_positif(jumlah, "jumlah")

    def hitung_subtotal(self):
        """Harga menu x jumlah porsi."""
        return self.menu.harga * self.jumlah

    def to_line(self):
        """Ubah pesanan menjadi satu baris teks untuk disimpan ke file."""
        return (f"{self.id};{self.pelanggan};{self.menu.kode};"
                f"{self.menu.nama};{self.jumlah};{self.hitung_subtotal()}")
