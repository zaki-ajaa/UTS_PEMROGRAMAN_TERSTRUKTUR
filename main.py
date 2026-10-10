"""main.py - program utama: sistem pemesanan dimsum."""
from dimsum import fileio, processing
from dimsum.models import Pesanan
from dimsum.validasi import DataTidakValid, validasi_tidak_kosong, validasi_angka_positif

FILE_MENU = "data/menu.txt"
FILE_PESANAN = "data/pesanan.txt"
FILE_LAPORAN = "data/laporan_penjualan.txt"


def tampilkan_menu(menu):
    """Menampilkan daftar menu."""
    print("\n=== MENU DIMSUM ===")
    for k, m in menu.items():
        print(f"{k}  {m.nama:<20} Rp{m.harga:>7,}  [{m.atribut.get('kategori')}]")


def tambah_pesanan(menu):
    """Input pelanggan -> validasi -> simpan (mode 'a')."""
    try:
        nama = validasi_tidak_kosong(input("Nama pelanggan : "), "pelanggan")
        kode = input("Kode menu      : ").strip().upper()
        if kode not in menu:
            raise DataTidakValid(f"Kode menu '{kode}' tidak ada")
        jumlah = validasi_angka_positif(input("Jumlah porsi   : "))
    except DataTidakValid as e:
        print("Input ditolak:", e)
        return
    id_baru = len(fileio.baca_pesanan(FILE_PESANAN, menu)) + 1
    p = Pesanan(id_baru, nama, menu[kode], jumlah)
    fileio.simpan_pesanan(p, FILE_PESANAN)
    print(f"Pesanan #{id_baru} tersimpan. Subtotal Rp{p.hitung_subtotal():,}")


def main():
    if fileio.buat_file_menu(FILE_MENU):                 # mode 'x'
        print("File menu dibuat pertama kali.")
    menu = fileio.baca_menu(FILE_MENU)
    while True:
        print("\n1.Lihat menu 2.Tambah pesanan 3.Lihat pesanan "
              "4.Buat laporan 0.Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "1":
            tampilkan_menu(menu)
        elif pilih == "2":
            tambah_pesanan(menu)
        elif pilih == "3":
            for p in fileio.baca_pesanan(FILE_PESANAN, menu):
                print(p.to_line())
        elif pilih == "4":
            teks = processing.buat_laporan(fileio.baca_pesanan(FILE_PESANAN, menu))
            fileio.tulis_laporan(teks, FILE_LAPORAN)     # mode 'w'
            print(teks)
        elif pilih == "0":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid")


if __name__ == "__main__":
    main()
