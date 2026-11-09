# Ketupat: Pemodelan Topologi dan Penguraian Graf

Kod pengesahan bagi manuskrip **"Pemodelan topologi dan penguraian graf dalam anyaman ketupat tradisional: teorem, pengiraan dan pengesahan komputeran"** oleh Zainor Ridzuan Yahya, Zainab Yahya dan Zabidi Abu Hasan (Universiti Malaysia Perlis), dihantar ke *Sains Malaysiana*.

Setiap nilai berangka dalam manuskrip dilindungi oleh `assert` dalam salah satu skrip di bawah. Jika skrip selesai tanpa ralat, kesemua dakwaannya lulus.

*English:* Python scripts that verify every numerical claim in the manuscript and regenerate its figures. Install the requirements and run `python jalankan_semua.py`.

## Cara menjalankan

Keperluan: Python 3.9 atau lebih baharu.

```bash
pip install -r requirements.txt
python jalankan_semua.py    # ~1 minit
```

Output yang dijangka:

```
LULUS     0.5 s  03_Kod/verify_octahedron.py
...
Semua skrip lulus. Rajah disimpan dalam 02_Rajah/, log dalam hasil/.
```

Setiap skrip juga boleh dijalankan sendiri dari dalam folder `03_Kod/`.

## Padanan skrip dengan manuskrip

| Skrip | Bahagian manuskrip | Dakwaan yang disahkan |
|---|---|---|
| `verify_octahedron.py` | Model 2-Daun | Oktahedron 4-sekata (V=6, E=12, F=8); model 2-daun ialah dua kitaran sisi-asing yang meliputi semua sisi |
| `verify_cuboctahedron.py` | Model 3-Daun | Kuboktahedron (V=12, E=24, F=14); model 3-daun lulus Definisi 2 |
| `verify_keluarga_n_daun.py` | Keluarga Penuh Anyaman Seimbang | Syarat perlu n \| E dan 3 ≤ E/n ≤ V; n ∈ {2, 3, 4, 6, 8} semuanya wujud |
| `verify_laluan_terus.py` | Sistem Peralihan; Analisis Laluan Terus | Bilangan bucu terus dan lipatan bagi model 2-daun dan 3-daun |
| `verify_antiprisma_heksagon.py` | Anyaman Tanpa Lipatan pada Keluarga Antiprisma | Antiprisma heksagon: 134 penguraian 3-daun seimbang, laluan terus memberi tiga kitaran 8-sisi; oktahedron: 6 penguraian 2-daun |
| `verify_semakan_silang.py` | Protokol Pengesahan; Analisis Laluan Terus; Antiprisma | Sistem peralihan = exact cover (43 / 3217 / 2169); Jadual 4; Proposisi 2 bagi 3 ≤ m ≤ 15; sifat Brunnian bagi m = 3, 6, 9, 12 |
| `verify_ralat_percubaan_pertama.py` | Analisis Ralat | 3 segmen palsu, 2 sisi bertindih, 7 sisi tercicir |
| `verify_graf_medial.py` | Skop dan Had Rangka Kerja | M(tetrahedron) = oktahedron, M(kubus) = kuboktahedron, M(piramid m-gon) = antiprisma m-gon |
| `verify_bentuk_lain.py` | Skop dan Had Rangka Kerja | Tetrahedron dan prisma tidak 4-sekata, jadi tidak boleh dipadankan terus dengan Ketupat Palas dan Ketupat Pasar |
| `generate_figures.py` | Rajah 1, 2, 3, 5 | Menjana rajah daripada graf yang telah disahkan |
| `generate_figure5.py` | Rajah 4 | Anyaman tanpa lipatan pada antiprisma heksagon |

Nota nama fail: `figure4_analisis_ralat.png` muncul sebagai Rajah 5 dalam manuskrip, dan `figure5_antiprisma_heksagon.png` sebagai Rajah 4. Nama fail dikekalkan supaya tidak memecahkan rujukan lama.

Panel (c) Rajah 1 menggunakan foto ketupat milik penulis yang tidak disertakan di sini. Tanpa foto itu, `generate_figures.py` menjana versi dua panel (`figure1_oktahedron.png`).

## Penggunaan AI

Skrip dalam repositori ini ditulis dengan bantuan alat AI perbualan, seperti yang diisytiharkan dalam manuskrip. Para penulis telah menjalankan semula kesemua skrip dan menyemak outputnya terhadap teks.

## Petikan

Sila petik manuskrip dan repositori ini. Maklumat petikan ada dalam `CITATION.cff` (butang "Cite this repository" di GitHub) dan pada rekod Zenodo.

## Lesen

MIT. Lihat `LICENSE`.
