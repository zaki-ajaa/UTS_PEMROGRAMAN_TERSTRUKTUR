"""fileio.py - semua operasi baca/tulis/tambah file (selalu with open)."""
import os
from dimsum.models import MenuItem, Pesanan
from dimsum.validasi import DataTidakValid

MENU_AWAL = [
    "HG01;Hakau Udang;18000;Kukus",
    "SM02;Siomay Ayam;15000;Kukus",
    "BP03;Bakpao Babi Kecap;16000;Kukus",
    "LM04;Lumpia Udang;17000;Goreng",
    "XL05;Xiao Long Bao;22000;Kukus",
    "CK06;Cakwe Isi Udang;14000;Goreng",
]


def buat_menu_dari_baris(baris):
    """Ubah satu baris file menjadi objek MenuItem (salah format -> raise)."""
    bagian = baris.strip().split(";")
    if len(bagian) != 4:
        raise DataTidakValid(f"Format menu salah: {baris.strip()!r}")
    kode, nama, harga, kategori = bagian
    return MenuItem(kode, nama, harga, kategori=kategori)


def buat_pesanan_dari_baris(baris, daftar_menu):
    """Ubah satu baris file menjadi objek Pesanan (salah format -> raise)."""
    bagian = baris.strip().split(";")
    if len(bagian) != 6:
        raise DataTidakValid(f"Format pesanan salah: {baris.strip()!r}")
    id_p, pelanggan, kode, _nama, jumlah, _subtotal = bagian
    menu = daftar_menu.get(kode)
    if menu is None:
        raise DataTidakValid(f"Kode menu tidak dikenal: {kode!r}")
    return Pesanan(int(id_p), pelanggan, menu, jumlah)


def buat_file_menu(path):
    """Mode 'x': buat file menu pertama kali, TIDAK menimpa jika sudah ada."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    try:
        with open(path, "x", encoding="utf-8") as f:
            f.write("\n".join(MENU_AWAL) + "\n")
        return True
    except FileExistsError:
        return False            # sudah ada -> aman, data lama tidak berubah


def baca_menu(path):
    """Mode 'r' iteratif: hasilnya dict {kode: MenuItem}. Baris rusak dilewati."""
    menu = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for baris in f:                         # pembacaan per baris
                if not baris.strip():
                    continue
                try:
                    item = buat_menu_dari_baris(baris)
                    menu[item.kode] = item
                except DataTidakValid as e:         # lewati, jangan berhenti
                    print(f"[dilewati] {e}")
    except FileNotFoundError:
        print(f"Error: file menu '{path}' belum ada. Jalankan inisialisasi dulu.")
    return menu


def simpan_pesanan(pesanan, path):
    """Mode 'a': tambah satu pesanan di akhir tanpa menghapus data lama."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(pesanan.to_line() + "\n")


def baca_pesanan(path, daftar_menu):
    """Mode 'r' iteratif: list Pesanan. Baris rusak dilewati."""
    hasil = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for baris in f:
                if not baris.strip():
                    continue
                try:
                    hasil.append(buat_pesanan_dari_baris(baris, daftar_menu))
                except (DataTidakValid, ValueError) as e:
                    print(f"[dilewati] {e}")
    except FileNotFoundError:
        print(f"Error: file pesanan '{path}' belum ada (belum ada pesanan).")
    return hasil


def tulis_laporan(teks, path):
    """Mode 'w': laporan selalu dibuat baru (versi lama diganti)."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(teks)
