"""
Diagnostik penuh: Percubaan 3-Daun PERTAMA (sebelum pembetulan).
Rujuk Contoh 6 (bahagian 'Analisis Ralat') dalam manuskrip.
Label bucu 0-11 ialah indeks baris dalam tatasusunan `bucu` di bawah; label inilah
yang digunakan dalam teks manuskrip (segmen {1,2}, {4,8}, {5,9}; muka {1,5,2,9}; sisi {2,11}, {3,11}).

Kod ini mengesahkan bahawa percubaan pertama gagal atas TIGA sebab serentak:
  (a) 3 "sisi palsu" (phantom edges) - segmen garis yang dilukis tetapi
      BUKAN sisi kuboktahedron sebenar (ia adalah pepenjuru muka segi empat)
  (b) 2 sisi sah yang bertindih (dilukis oleh dua daun berlainan)
  (c) 7 sisi sah yang tercicir (tidak dilukis langsung oleh mana-mana daun)
Ketiga-tiga nombor ini disemak secara bebas pada penghujung skrip (senarai eksplisit
sisi tercicir dan semakan darjah setiap bucu), bukan sekadar identiti aritmetik.
"""
import numpy as np
import networkx as nx
from itertools import combinations

bucu = np.array([
    [ 1, 1, 0], [-1, 1, 0], [-1,-1, 0], [ 1,-1, 0],
    [ 1, 0, 1], [-1, 0, 1], [ 0, 1, 1], [ 0,-1, 1],
    [ 1, 0,-1], [-1, 0,-1], [ 0, 1,-1], [ 0,-1,-1],
], dtype=float)
n = len(bucu)

dists = {}
for i, j in combinations(range(n), 2):
    dists[(i, j)] = round(np.linalg.norm(bucu[i]-bucu[j]), 6)
min_d = min(dists.values())
edges = sorted([e for e, d in dists.items() if abs(d-min_d) < 1e-6])
G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(edges)
E_full = set(tuple(sorted(e)) for e in G.edges())
assert len(E_full) == 24

def path_to_edges(path):
    return [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]

# Tiga laluan seperti yang dicadangkan pada percubaan pertama (fasa penerokaan)
daun_1 = [0, 6, 1, 5, 2, 11, 3, 8, 0]
daun_2 = [1, 10, 0, 4, 7, 3, 11, 2, 1]
daun_3 = [4, 6, 5, 9, 10, 8, 4]
paths = {"Daun 1": daun_1, "Daun 2": daun_2, "Daun 3": daun_3}

print("=== DIAGNOSTIK PERCUBAAN 3-DAUN PERTAMA (CACAT) ===\n")

all_segments = []
for name, p in paths.items():
    segs = path_to_edges(p)
    valid = [e for e in segs if e in E_full]
    phantom = [e for e in segs if e not in E_full]
    print(f"{name}: {len(segs)} segmen dilukis -> {len(valid)} sah, {len(phantom)} PALSU {phantom}")
    all_segments.extend(segs)

print(f"\nJumlah keseluruhan segmen dilukis (3 daun): {len(all_segments)}")

valid_segments = [e for e in all_segments if e in E_full]
phantom_segments = [e for e in all_segments if e not in E_full]
print(f"  - segmen sah (edge sebenar graf)   : {len(valid_segments)}")
print(f"  - segmen PALSU (phantom, non-edge) : {len(phantom_segments)}  -> {phantom_segments}")

covered_unique = set(valid_segments)
n_duplicate = len(valid_segments) - len(covered_unique)
print(f"  - sisi sah UNIK diliputi            : {len(covered_unique)}")
print(f"  - sisi sah BERTINDIH (dikira 2x)    : {n_duplicate}")

missing = E_full - covered_unique
print(f"  - sisi sah TERCICIR (0x dilukis)    : {len(missing)} -> {sorted(missing)}")

# Nilai yang dilaporkan dalam manuskrip
assert sorted(phantom_segments) == [(1, 2), (4, 8), (5, 9)]
assert n_duplicate == 2
dup = sorted(e for e in covered_unique if valid_segments.count(e) == 2)
assert dup == [(2, 11), (3, 11)]
assert sorted(missing) == [(1, 9), (2, 7), (2, 9), (3, 4), (5, 7), (8, 11), (9, 11)]
# {1,2} dan {5,9} ialah kedua-dua pepenjuru muka segi empat {1,5,2,9} (satah x = -1)
assert all(bucu[v][0] == -1 for v in (1, 5, 2, 9))
# Pepenjuru terletak pada permukaan (satah muka); palsu kerana bukan sisi graf
for a, b in phantom_segments:
    assert abs(np.linalg.norm(bucu[a] - bucu[b]) - 2.0) < 1e-9

print("\n--- Semakan bebas ---")
# Semakan darjah: kira terus di setiap bucu berapa sisi sah unik yang dilukis
deg_U = {v: sum(1 for e in covered_unique if v in e) for v in range(n)}
kurang = sum(4 - deg_U[v] for v in range(n))
print(f"Jumlah (4 - deg_U(v)) ke atas semua bucu = {kurang}  (mesti = 2 x 7 = 14)")
assert kurang == 2 * 7
print(f"Senarai eksplisit 7 sisi tercicir: {sorted(missing)}")

print("\n--- Semakan aritmetik silang ---")
lhs = len(covered_unique) + len(missing)
print(f"|sisi unik diliputi| + |tercicir| = {len(covered_unique)} + {len(missing)} = {lhs}  (mesti = |E| = {len(E_full)})")
assert lhs == len(E_full)

lhs2 = len(valid_segments) + len(phantom_segments)
print(f"|segmen sah| + |segmen palsu| = {len(valid_segments)} + {len(phantom_segments)} = {lhs2}  (mesti = jumlah segmen = {len(all_segments)})")
assert lhs2 == len(all_segments)

print("\n=== KESIMPULAN ===")
print(f"Percubaan pertama GAGAL kerana ketiga-tiga sebab serentak:")
print(f"  1. {len(phantom_segments)} sisi PALSU dilukis (pepenjuru muka segi empat: terletak pada permukaan, tetapi bukan sisi graf)")
print(f"  2. {n_duplicate} sisi SAH bertindih (dikongsi oleh 2 daun berlainan, melanggar syarat sisi-asing)")
print(f"  3. {len(missing)} sisi SAH langsung tidak dilukis (menyebabkan lubang/kebocoran)")
print("Ini konsisten dengan pemerhatian visual asal: bentuk kelihatan 'terbuka'/bocor")
print("kerana gabungan pepenjuru yang memotong lintang petak anyaman dan ruang kosong sebenar.")
