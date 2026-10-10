"""validasi.py - pengecekan input dan data."""


class DataTidakValid(Exception):
    """Exception buatan sendiri untuk data/input yang tidak valid."""


def validasi_tidak_kosong(nilai, nama_field):
    """Memastikan field tidak kosong; jika kosong -> raise exception buatan."""
    if nilai is None or str(nilai).strip() == "":
        raise DataTidakValid(f"Field '{nama_field}' tidak boleh kosong")
    return str(nilai).strip()


def validasi_angka_positif(teks, nama_field="jumlah"):
    """Mengubah teks ke int dan memastikan > 0."""
    try:
        angka = int(teks)                      # bisa ValueError ("abc")
    except ValueError:
        raise DataTidakValid(f"'{nama_field}' harus berupa angka bulat: {teks!r}")
    if angka <= 0:                             # nilai negatif / nol ditolak
        raise DataTidakValid(f"'{nama_field}' harus lebih dari 0: {angka}")
    return angka


if __name__ == "__main__":
    # pengujian lokal: hanya jalan bila file ini dijalankan langsung
    assert validasi_angka_positif("3") == 3
    try:
        validasi_angka_positif("-1")
    except DataTidakValid as e:
        print("OK, error tertangkap:", e)
    print("validasi.py lulus pengujian lokal")
