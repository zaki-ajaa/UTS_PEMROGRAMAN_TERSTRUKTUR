"""processing.py - perhitungan dan analisis data pesanan."""


def hitung_total(*subtotal):
    """*args: jumlah subtotal bebas. assert memastikan tidak ada yang negatif."""
    assert all(s >= 0 for s in subtotal), "subtotal tidak boleh negatif"
    return sum(subtotal)


def total_per_menu(daftar_pesanan):
    """Mengelompokkan jumlah porsi per nama menu -> dict {nama: porsi}."""
    hasil = {}
    for p in daftar_pesanan:
        hasil[p.menu.nama] = hasil.get(p.menu.nama, 0) + p.jumlah
    return hasil


def menu_terlaris(daftar_pesanan, n=3):
    """Mengurutkan menu dari porsi terbanyak; lambda sebagai key sorted()."""
    per_menu = total_per_menu(daftar_pesanan)
    urut = sorted(per_menu.items(), key=lambda kv: kv[1], reverse=True)
    return urut[:n]


def filter_pelanggan(daftar_pesanan, nama):
    """Filter pesanan milik satu pelanggan (lambda + filter)."""
    return list(filter(lambda p: p.pelanggan.lower() == nama.lower(),
                       daftar_pesanan))


def buat_laporan(daftar_pesanan):
    """Menyusun teks laporan penjualan lengkap."""
    if not daftar_pesanan:
        return "LAPORAN PENJUALAN DIMSUM\nBelum ada pesanan.\n"
    total = hitung_total(*[p.hitung_subtotal() for p in daftar_pesanan])  # list -> *args
    baris = ["LAPORAN PENJUALAN DIMSUM", "=" * 40]
    for p in daftar_pesanan:
        baris.append(f"#{p.id:<3} {p.pelanggan:<10} {p.menu.nama:<20} "
                     f"x{p.jumlah:<2} Rp{p.hitung_subtotal():>8,}")
    baris += ["-" * 40, f"Jumlah transaksi : {len(daftar_pesanan)}",
              f"Total pendapatan : Rp{total:,}", "Menu terlaris    :"]
    for nama, porsi in menu_terlaris(daftar_pesanan, n=3):   # keyword argument
        baris.append(f"  - {nama} ({porsi} porsi)")
    return "\n".join(baris) + "\n"


if __name__ == "__main__":
    assert hitung_total(1000, 2000, 3000) == 6000
    print("processing.py lulus pengujian lokal")
