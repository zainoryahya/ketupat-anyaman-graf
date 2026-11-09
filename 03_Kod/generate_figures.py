"""
Jana rajah statik (PNG, resolusi tinggi) bagi kertas kerja:
  Rajah 1: Ketupat 2-Daun (Oktahedron) - rangka dawai berwarna + jaringan pejal
  Rajah 2: Ketupat 3-Daun (Kuboktahedron) - rangka dawai berwarna + jaringan pejal
  Rajah 3: Keluarga anyaman seimbang n=4, 6, 8 pada kuboktahedron
  Rajah 4 (fail figure4_analisis_ralat.png): analisis ralat - model cacat vs model sah

NOTA: dalam manuskrip, figure4_analisis_ralat.png muncul sebagai RAJAH 5, manakala
RAJAH 4 ialah figure5_antiprisma_heksagon.png (dijana oleh generate_figure5.py).
Nama fail dikekalkan supaya tidak memecahkan rujukan lama.

Kod ini menggunakan hanya struktur graf & bucu yang TELAH disahkan oleh
verify_octahedron.py dan verify_cuboctahedron.py.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import ConvexHull
from itertools import combinations

from pathlib import Path
# Simpan rajah ke ../02_Rajah/ relatif kepada lokasi skrip ini,
# supaya ia berfungsi pada mana-mana komputer tanpa suntingan.
OUT = str(Path(__file__).resolve().parent.parent / "02_Rajah") + "/"
Path(OUT).mkdir(parents=True, exist_ok=True)

def build_graph_edges(bucu):
    dists = {}
    for i, j in combinations(range(len(bucu)), 2):
        dists[(i, j)] = round(np.linalg.norm(bucu[i]-bucu[j]), 6)
    mind = min(dists.values())
    return sorted([e for e, d in dists.items() if abs(d-mind) < 1e-6])

def path_to_edges(path):
    return [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]

def style_axis(ax, title):
    ax.set_title(title, fontsize=11)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])

def draw_wireframe(ax, bucu, leaf_paths, colors, labels):
    ax.scatter(bucu[:,0], bucu[:,1], bucu[:,2], color='black', s=35, zorder=5)
    for path, c, lab in zip(leaf_paths, colors, labels):
        segs = [(bucu[a], bucu[b]) for a, b in path_to_edges(path)]
        lc = Line3DCollection(segs, colors=c, linewidths=3.2, label=lab)
        ax.add_collection3d(lc)
    ax.legend(loc='upper left', fontsize=8, frameon=False)

def draw_mesh(ax, bucu, face_color='#8FBF5C', edge_color='#2E5B1A'):
    hull = ConvexHull(bucu)
    faces = [bucu[s] for s in hull.simplices]
    mesh = Poly3DCollection(faces, facecolor=face_color, edgecolor=edge_color,
                             linewidths=0.8, alpha=1.0)
    ax.add_collection3d(mesh)
    mins, maxs = bucu.min(0), bucu.max(0)
    for i, setter in enumerate([ax.set_xlim, ax.set_ylim, ax.set_zlim]):
        setter(mins[i]-0.3, maxs[i]+0.3)

# ================= RAJAH 1: Oktahedron (2 daun) =================
bucu_okta = np.array([
    [ 1, 0, 0], [-1, 0, 0], [ 0, 1, 0], [ 0,-1, 0], [ 0, 0, 1], [ 0, 0,-1],
], dtype=float)
daun_1 = [4, 0, 3, 5, 2, 1, 4]
daun_2 = [4, 2, 0, 5, 1, 3, 4]

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
draw_wireframe(ax1, bucu_okta, [daun_1, daun_2],
               ['#CC3333', '#1C4E9C'], ['Daun 1', 'Daun 2'])
for i, setter in enumerate([ax1.set_xlim, ax1.set_ylim, ax1.set_zlim]):
    setter(-1.3, 1.3)
style_axis(ax1, "(a) Rangka kitaran Euler 2 daun")

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
draw_mesh(ax2, bucu_okta)
style_axis(ax2, "(b) Jaringan pejal (kelongsong tertutup)")

fig.suptitle("Model Ketupat 2-Daun: Oktahedron (V=6, E=12, F=8)", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT + "figure1_oktahedron.png", dpi=220, bbox_inches='tight')
plt.close(fig)
print("Rajah 1 (2 panel model) disimpan.")

# ===== RAJAH 1 versi 3 panel: model + foto ketupat fizikal =====
# Panel (c) menuntut HANYA apa yang disokong oleh foto: dua helai berbeza warna.
# Bilangan persilangan pada ketupat fizikal jauh lebih besar daripada V=6 --
# lihat subseksyen "Resolusi model" dalam manuskrip.
FOTO = Path(__file__).resolve().parent.parent / "06_Gambar_Ketupat" / "KB_merah-putih_muka_03.jpeg"
if FOTO.exists():
    import matplotlib.image as mpimg
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(12.4, 4.6))
    gs = GridSpec(1, 3, width_ratios=[1.0, 1.0, 0.82], wspace=0.02,
                  left=0.01, right=0.99, top=0.86, bottom=0.02)

    ax1 = fig.add_subplot(gs[0], projection='3d')
    draw_wireframe(ax1, bucu_okta, [daun_1, daun_2],
                   ['#CC3333', '#1C4E9C'], ['Daun 1', 'Daun 2'])
    for setter in [ax1.set_xlim, ax1.set_ylim, ax1.set_zlim]:
        setter(-0.85, 0.85)
    ax1.set_axis_off(); ax1.set_box_aspect([1, 1, 1])
    ax1.set_title("(a) Model: rangka dua kitaran tertutup", fontsize=10.5, pad=0)

    ax2 = fig.add_subplot(gs[1], projection='3d')
    draw_mesh(ax2, bucu_okta)
    for setter in [ax2.set_xlim, ax2.set_ylim, ax2.set_zlim]:
        setter(-0.85, 0.85)
    ax2.set_axis_off(); ax2.set_box_aspect([1, 1, 1])
    ax2.set_title("(b) Model: jaringan pejal", fontsize=10.5, pad=0)

    ax3 = fig.add_subplot(gs[2])
    img = mpimg.imread(str(FOTO))
    ax3.imshow(img); ax3.set_axis_off()
    ax3.set_title("(c) Ketupat fizikal: dua helai", fontsize=10.5, pad=4)
    H, W = img.shape[0], img.shape[1]
    anot = dict(fontsize=8.5, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.45", alpha=0.94))
    # Helai merah: reben besar melengkung di bawah kiri
    ax3.annotate("Helai 1", xy=(0.20*W, 0.90*H), xytext=(0.50*W, 0.97*H),
                 color="#B03030",
                 arrowprops=dict(arrowstyle="->", lw=1.5, color="#B03030"), **anot)
    # Helai putih: reben di bahagian atas
    ax3.annotate("Helai 2", xy=(0.44*W, 0.05*H), xytext=(0.70*W, 0.14*H),
                 color="#333333",
                 arrowprops=dict(arrowstyle="->", lw=1.5, color="#333333"), **anot)

    fig.suptitle("Ketupat 2-Daun: Model Beresolusi Minimum berbanding Objek Fizikal",
                 fontsize=12, fontweight='bold', y=0.975)
    plt.savefig(OUT + "figure1b_model_vs_fizikal.png", dpi=220, bbox_inches='tight')
    plt.close(fig)
    print("Rajah 1b (model + foto fizikal) disimpan.")
else:
    print("AMARAN: foto tidak dijumpai -- Rajah 1b dilangkau.")

# ================= RAJAH 2: Kuboktahedron (3 daun, sah) =================
bucu_kubo = np.array([
    [ 1, 1, 0], [-1, 1, 0], [-1,-1, 0], [ 1,-1, 0],
    [ 1, 0, 1], [-1, 0, 1], [ 0, 1, 1], [ 0,-1, 1],
    [ 1, 0,-1], [-1, 0,-1], [ 0, 1,-1], [ 0,-1,-1],
], dtype=float)
daun_1k = [0, 4, 3, 8, 10, 9, 1, 6, 0]
daun_2k = [2, 5, 6, 4, 7, 3, 11, 9, 2]
daun_3k = [0, 8, 11, 2, 7, 5, 1, 10, 0]

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
draw_wireframe(ax1, bucu_kubo, [daun_1k, daun_2k, daun_3k],
               ['#CC3333', '#1C4E9C', '#D8A11B'], ['Daun 1', 'Daun 2', 'Daun 3'])
for i, setter in enumerate([ax1.set_xlim, ax1.set_ylim, ax1.set_zlim]):
    setter(-1.3, 1.3)
style_axis(ax1, "(a) Rangka penguraian 3 kitaran 8-sisi")

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
draw_mesh(ax2, bucu_kubo, face_color='#8FBF5C', edge_color='#2E5B1A')
style_axis(ax2, "(b) Jaringan pejal (14 muka: 8 segi tiga, 6 segi empat)")

fig.suptitle("Model Ketupat 3-Daun: Kuboktahedron (V=12, E=24, F=14)", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT + "figure2_kuboktahedron.png", dpi=220, bbox_inches='tight')
plt.close(fig)
print("Rajah 2 disimpan.")

# ===== RAJAH 5 manuskrip (fail figure4_analisis_ralat.png): analisis ralat =====
d1_bad = [0, 6, 1, 5, 2, 11, 3, 8, 0]
d2_bad = [1, 10, 0, 4, 7, 3, 11, 2, 1]
d3_bad = [4, 6, 5, 9, 10, 8, 4]

edges_all = set(tuple(sorted(e)) for e in build_graph_edges(bucu_kubo))

# Asingkan setiap segmen laluan kepada: sah (valid, ada dalam graf sebenar)
# atau palsu/phantom (invalid, bukan sisi kuboktahedron sebenar - pepenjuru muka segi empat)
def split_valid_invalid(paths, edges_all):
    valid, invalid = [], []
    for p in paths:
        for e in path_to_edges(p):
            (valid if e in edges_all else invalid).append(e)
    return valid, invalid

all_drawn_valid, phantom_edges = split_valid_invalid([d1_bad, d2_bad, d3_bad], edges_all)
covered_valid = set(all_drawn_valid)
missing = edges_all - covered_valid
n_dup = len(all_drawn_valid) - len(covered_valid)

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.scatter(bucu_kubo[:,0], bucu_kubo[:,1], bucu_kubo[:,2], color='black', s=35, zorder=5)
for p, c, lab in zip([d1_bad, d2_bad, d3_bad], ['#CC3333', '#1C4E9C', '#D8A11B'],
                      ['Daun 1', 'Daun 2', 'Daun 3']):
    segs = [(bucu_kubo[a], bucu_kubo[b]) for a, b in path_to_edges(p) if (a, b) in edges_all]
    ax1.add_collection3d(Line3DCollection(segs, colors=c, linewidths=3.0, label=lab))
phantom_segs = [(bucu_kubo[a], bucu_kubo[b]) for a, b in phantom_edges]
ax1.add_collection3d(Line3DCollection(phantom_segs, colors='magenta', linewidths=2.0,
                                       linestyles='dotted', label=f'Sisi palsu/phantom ({len(phantom_edges)})'))
missing_segs = [(bucu_kubo[a], bucu_kubo[b]) for a, b in missing]
ax1.add_collection3d(Line3DCollection(missing_segs, colors='black', linewidths=2.2,
                                       linestyles='dashed', label=f'Sisi tercicir ({len(missing)})'))
for i, setter in enumerate([ax1.set_xlim, ax1.set_ylim, ax1.set_zlim]):
    setter(-1.3, 1.3)
ax1.legend(loc='upper left', fontsize=7, frameon=False)
style_axis(ax1, f"(a) Percubaan cacat: {len(phantom_edges)} sisi palsu,\n{n_dup} sisi bertindih, {len(missing)} sisi tercicir")

print(f"\n[Diagnostik analisis ralat] sisi palsu={len(phantom_edges)} {phantom_edges}, "
      f"bertindih={n_dup}, tercicir={len(missing)} {sorted(missing)}")

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
draw_wireframe(ax2, bucu_kubo, [daun_1k, daun_2k, daun_3k],
               ['#CC3333', '#1C4E9C', '#D8A11B'], ['Daun 1', 'Daun 2', 'Daun 3'])
for i, setter in enumerate([ax2.set_xlim, ax2.set_ylim, ax2.set_zlim]):
    setter(-1.3, 1.3)
style_axis(ax2, "(b) Model diperbetulkan: 0 sisi tercicir\n(lulus Definisi 2)")

fig.suptitle("Perbandingan: Kegagalan Kitaran Euler lawan Model Sah", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT + "figure4_analisis_ralat.png", dpi=220, bbox_inches='tight')
plt.close(fig)
print("Rajah analisis ralat (figure4_*) disimpan.")

# ========= RAJAH 3: Keluarga anyaman seimbang n=4, 6, 8 =========
# Penguraian ini dijumpai & disahkan secara tuntas oleh verify_keluarga_n_daun.py
keluarga = {
    # n=4: empat khatulistiwa heksagon SEBENAR (setiap satu terletak pada satu
    # satah melalui pusat). Ini juga penguraian LALUAN-TERUS -- lihat
    # verify_laluan_terus.py. Jalur tidak pernah membelok pada mana-mana silangan.
    4: [[(0,4),(0,10),(9,10),(2,9),(2,7),(4,7)],
        [(3,4),(4,6),(1,6),(1,9),(9,11),(3,11)],
        [(3,7),(5,7),(1,5),(1,10),(8,10),(3,8)],
        [(0,8),(0,6),(5,6),(2,5),(2,11),(8,11)]],
    6: [[(0,4),(0,8),(3,4),(3,8)],
        [(0,6),(0,10),(1,6),(1,10)],
        [(1,5),(1,9),(2,5),(2,9)],
        [(2,7),(2,11),(3,7),(3,11)],
        [(4,6),(4,7),(5,6),(5,7)],
        [(8,10),(8,11),(9,10),(9,11)]],
    8: [[(0,4),(0,6),(4,6)],
        [(0,8),(0,10),(8,10)],
        [(1,5),(1,6),(5,6)],
        [(1,9),(1,10),(9,10)],
        [(2,5),(2,7),(5,7)],
        [(2,9),(2,11),(9,11)],
        [(3,4),(3,7),(4,7)],
        [(3,8),(3,11),(8,11)]],
}
subtajuk = {4: "(a) n=4: empat khatulistiwa heksagon\n(penguraian laluan-terus)",
            6: "(b) n=6: enam kitaran 4-sisi\n(muka segi empat)",
            8: "(c) n=8: lapan kitaran 3-sisi\n(muka segi tiga)"}
palet = ['#CC3333', '#1C4E9C', '#D8A11B', '#2E8B57', '#8B008B', '#FF8C00',
         '#00868B', '#8B4513']

# Semakan integriti sebelum melukis: sisi-asing + liputan penuh
for n, daun in keluarga.items():
    semua = [tuple(sorted(e)) for d in daun for e in d]
    assert len(semua) == len(set(semua)) == 24, f"n={n}: bukan sisi-asing/liputan penuh"
    assert set(semua) == edges_all, f"n={n}: sisi tidak sepadan graf sebenar"
    assert all(len(d) == 24 // n for d in daun), f"n={n}: daun tidak seimbang"
print("[Rajah 3] Ketiga-tiga penguraian n=4, 6, 8 lulus semakan sisi-asing & liputan penuh.")

fig = plt.figure(figsize=(12, 5.0))
for k, n in enumerate([4, 6, 8]):
    ax = fig.add_subplot(1, 3, k + 1, projection='3d')
    ax.scatter(bucu_kubo[:,0], bucu_kubo[:,1], bucu_kubo[:,2],
               color='black', s=22, zorder=5)
    for idx, daun in enumerate(keluarga[n]):
        segs = [(bucu_kubo[a], bucu_kubo[b]) for a, b in daun]
        ax.add_collection3d(Line3DCollection(segs, colors=palet[idx % len(palet)],
                                             linewidths=3.0))
    for setter in [ax.set_xlim, ax.set_ylim, ax.set_zlim]:
        setter(-1.15, 1.15)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    ax.set_title(subtajuk[n], fontsize=10.5, pad=-2)

fig.suptitle("Keluarga Anyaman Seimbang pada Kuboktahedron (setiap warna = satu helai daun)",
             fontsize=12, fontweight='bold', y=0.99)
plt.tight_layout(rect=[0, 0.02, 1, 0.93])
plt.subplots_adjust(wspace=0.0)
plt.savefig(OUT + "figure3_keluarga_n_daun.png", dpi=220, bbox_inches='tight')
plt.close(fig)
print("Rajah 3 disimpan.")

# ---- Pangkas jidar putih supaya rajah padat dalam manuskrip ----
try:
    from PIL import Image, ImageChops
    import glob as _glob
    for _f in sorted(_glob.glob(OUT + "figure*.png")):
        _im = Image.open(_f).convert("RGB")
        _bb = ImageChops.difference(
            _im, Image.new("RGB", _im.size, (255, 255, 255))).getbbox()
        if _bb:
            _im.crop(_bb).save(_f)
    print("Semua rajah dipangkas (jidar putih dibuang).")
except ImportError:
    print("AMARAN: Pillow tiada -- rajah tidak dipangkas.")

print("\nSemua rajah berjaya dijana.")
