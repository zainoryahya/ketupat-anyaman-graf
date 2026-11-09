# -*- coding: utf-8 -*-
"""
Jalankan kesemua skrip pengesahan dan penjanaan rajah, kemudian cetak ringkasan.

    python jalankan_semua.py    # ~1 minit

Setiap skrip pengesahan menggunakan `assert`: kod keluar 0 bermakna kesemua dakwaan
lulus. Output penuh setiap skrip disimpan dalam folder hasil/.
"""
import subprocess
import sys
import time
from pathlib import Path

AKAR = Path(__file__).resolve().parent
HASIL = AKAR / "hasil"

UTAMA = [
    "verify_octahedron.py",
    "verify_cuboctahedron.py",
    "verify_keluarga_n_daun.py",
    "verify_laluan_terus.py",
    "verify_antiprisma_heksagon.py",
    "verify_semakan_silang.py",
    "verify_ralat_percubaan_pertama.py",
    "verify_graf_medial.py",
    "verify_bentuk_lain.py",
    "generate_figures.py",
    "generate_figure5.py",
]


def jalan(folder, skrip):
    t0 = time.time()
    p = subprocess.run([sys.executable, skrip], cwd=folder, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    masa = time.time() - t0
    (HASIL / (Path(skrip).stem + ".txt")).write_text(p.stdout + p.stderr, encoding="utf-8")
    return p.returncode == 0, masa


def main():
    HASIL.mkdir(exist_ok=True)
    senarai = [(AKAR / "03_Kod", s) for s in UTAMA]
    gagal = 0
    for folder, s in senarai:
        ok, masa = jalan(folder, s)
        gagal += not ok
        print(f"{'LULUS' if ok else 'GAGAL':6s} {masa:6.1f} s  {folder.name}/{s}")
    print("-" * 50)
    if gagal:
        print(f"{gagal} skrip gagal. Lihat folder hasil/ untuk butiran.")
        sys.exit(1)
    print("Semua skrip lulus. Rajah disimpan dalam 02_Rajah/, log dalam hasil/.")


if __name__ == "__main__":
    main()
