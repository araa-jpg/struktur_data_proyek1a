"""
benchmark.py
Mengukur waktu operasi sisip, cari, hapus, dan tampil semua pada tiga struktur data.

Jalankan:  python benchmark.py
"""

import random
import time

from inventaris import (Produk, InventarisHashTable, InventarisArray,
                        InventarisSortedArray, InventarisLinkedList)

UKURAN = [1_000, 10_000, 50_000]   # jumlah produk di inventaris
JUMLAH_OPERASI = 200               # banyaknya operasi yang diukur per percobaan
ULANGI = 5                         # percobaan diulang, diambil rata-rata
random.seed(42)

IMPLEMENTASI = {
    "Hash Table (dict)": InventarisHashTable,
    "Array List (list)": InventarisArray,
    "Linked List": InventarisLinkedList,
    "Sorted Array + bisect": InventarisSortedArray,
}


def buat_produk(nomor: list) -> list:
    return [Produk(f"P{i:08d}", f"Produk {i}", "Umum", 10_000 + i, 10) for i in nomor]


def rata_rata_ms(fungsi) -> float:
    """Waktu rata-rata (milidetik) per satu operasi."""
    total = 0.0
    for _ in range(ULANGI):
        total += fungsi()
    return total / ULANGI / JUMLAH_OPERASI * 1000


def ukur(kelas, n: int) -> dict:
    nomor = list(range(0, 2 * n, 2))          # ID awal: genap
    random.shuffle(nomor)                     # urutan masuk acak
    dasar = buat_produk(nomor)
    id_acak = [p.id_produk for p in random.sample(dasar, JUMLAH_OPERASI)]
    # produk baru: ID ganjil, tersebar acak di antara ID yang sudah ada
    baru_tetap = buat_produk(random.sample(range(1, 2 * n, 2), JUMLAH_OPERASI))

    def siapkan():
        inv = kelas()
        inv.muat_massal(dasar)
        return inv

    def uji_sisip():                      # sisip produk baru (dengan cek ID unik)
        inv = siapkan()
        baru = baru_tetap
        t = time.perf_counter()
        for p in baru:
            inv.sisip(p)
        return time.perf_counter() - t

    def uji_cari():                       # cari ID acak yang ada
        inv = siapkan()
        t = time.perf_counter()
        for i in id_acak:
            inv.cari(i)
        return time.perf_counter() - t

    def uji_hapus():                      # hapus ID acak yang ada
        inv = siapkan()
        t = time.perf_counter()
        for i in id_acak:
            inv.hapus(i)
        return time.perf_counter() - t

    def uji_tampil():                     # tampil semua (dibagi JUMLAH_OPERASI di rata_rata_ms)
        inv = siapkan()
        t = time.perf_counter()
        for _ in range(JUMLAH_OPERASI):
            inv.semua()
        return time.perf_counter() - t

    return {
        "sisip": rata_rata_ms(uji_sisip),
        "cari": rata_rata_ms(uji_cari),
        "hapus": rata_rata_ms(uji_hapus),
        "tampil": rata_rata_ms(uji_tampil),
    }


def jalankan(ukuran=UKURAN) -> dict:
    """Mengembalikan {N: {nama_struktur: {operasi: ms}}} (dipakai juga untuk laporan)."""
    return {n: {nama: ukur(kelas, n) for nama, kelas in IMPLEMENTASI.items()} for n in ukuran}


def main() -> None:
    print(f"Benchmark: {JUMLAH_OPERASI} operasi per percobaan, "
          f"rata-rata {ULANGI} percobaan. Satuan: milidetik (ms) per operasi.\n")
    for n in UKURAN:
        print(f"=== N = {n:,} produk ===")
        print(f"{'Struktur Data':<24}{'Sisip':>12}{'Cari':>12}{'Hapus':>12}{'Tampil':>12}")
        for nama, kelas in IMPLEMENTASI.items():
            h = ukur(kelas, n)
            print(f"{nama:<24}{h['sisip']:>12.5f}{h['cari']:>12.5f}"
                  f"{h['hapus']:>12.5f}{h['tampil']:>12.5f}")
        print()


if __name__ == "__main__":
    main()
