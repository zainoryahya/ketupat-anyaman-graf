# -*- coding: utf-8 -*-
"""RAJAH 4 dalam manuskrip (fail figure5_*): anyaman 3-daun tanpa lipatan pada antiprisma heksagon.
Gaya mengikut Rajah 2 (generate_figures.py). Output: ../02_Rajah/figure5_antiprisma_heksagon.png
Data daun diambil terus daripada verify_antiprisma_heksagon.py (tiada laluan ditaip manual)."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_antiprisma_heksagon import antiprisma, bina_sisi, sistem_putaran, jejak, semak_definisi2

WARNA = ["#cc3333", "#1f4e9b", "#d9a21b"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "02_Rajah",
                   "figure5_antiprisma_heksagon.png")

P = antiprisma(6)
E = bina_sisi(P)
rot = sistem_putaran(P, E)
daun = jejak(rot, (0,) * len(P))           # laluan terus pada setiap bucu
semak_definisi2(E, daun, len(P))
assert sorted(len(L) for L in daun) == [8, 8, 8]

fig = plt.figure(figsize=(13, 5.2))
fig.suptitle("Ketupat 3-Daun Tanpa Lipatan: Antiprisma Heksagon (V=12, E=24, F=14)",
             fontweight="bold", fontsize=15, y=0.98)
elev, azim = 24, -70

ax = fig.add_subplot(1, 2, 1, projection="3d")
ax.set_title("(a) Tiga kitaran 8-sisi laluan terus (sifar lipatan)", fontsize=13)
for i, L in enumerate(daun):
    for k in range(len(L)):
        a, b = P[L[k]], P[L[(k + 1) % len(L)]]
        ax.plot(*zip(a, b), color=WARNA[i], lw=4.2, solid_capstyle="round",
                label=f"Daun {i+1}" if k == 0 else None)
ax.scatter(*P.T, color="black", s=28, depthshade=True, zorder=5)
ax.legend(loc="upper left", bbox_to_anchor=(-0.08, 1.0), frameon=False, fontsize=11)

ax2 = fig.add_subplot(1, 2, 2)
ax2.set_title("(b) Lukisan satah: gelang atas (dalam) dan bawah (luar)", fontsize=13)
# lukisan satah (gambar rajah Schlegel): gelang atas pada jejari 0.55, gelang bawah pada jejari 1.0
Q = P[:, :2] / np.linalg.norm(P[:, :2], axis=1, keepdims=True)
Q[:6] *= 0.55
for i, L in enumerate(daun):
    for k in range(len(L)):
        a, b = Q[L[k]], Q[L[(k + 1) % len(L)]]
        ax2.plot(*zip(a, b), color=WARNA[i], lw=3.2, solid_capstyle="round", alpha=0.9)
ax2.scatter(Q[:, 0], Q[:, 1], color="black", s=40, zorder=5)
for v, q in enumerate(Q):
    f = 0.72 if v < 6 else 1.13
    ax2.text(q[0] * f, q[1] * f, str(v), fontsize=10, ha="center", va="center")
ax2.set_aspect("equal"); ax2.set_axis_off()
ax2.set_xlim(-1.35, 1.35); ax2.set_ylim(-1.35, 1.35)

ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_zlim(-1.1, 1.1)
ax.set_box_aspect((1, 1, 1), zoom=1.45)
ax.view_init(elev=elev, azim=azim)
ax.set_axis_off()

plt.tight_layout(rect=(0, 0, 1, 0.95))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
plt.savefig(OUT, dpi=200, bbox_inches="tight")
print("Disimpan:", os.path.abspath(OUT))
