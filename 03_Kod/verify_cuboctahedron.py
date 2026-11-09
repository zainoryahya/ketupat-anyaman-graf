"""
Pengesahan model 3-daun pada kuboktahedron (bahagian 'Model 3-Daun' dalam manuskrip).
Sama seperti verify_octahedron.py tetapi bagi n=3 helai daun.
"""
import numpy as np
import networkx as nx
from itertools import combinations
from scipy.spatial import ConvexHull

bucu = np.array([
    [ 1, 1, 0], [-1, 1, 0], [-1,-1, 0], [ 1,-1, 0],   # 0-3 Ekuator (z=0)
    [ 1, 0, 1], [-1, 0, 1], [ 0, 1, 1], [ 0,-1, 1],    # 4-7 Satah atas (z=1)
    [ 1, 0,-1], [-1, 0,-1], [ 0, 1,-1], [ 0,-1,-1],    # 8-11 Satah bawah (z=-1)
], dtype=float)
n = len(bucu)

dists = {}
for i, j in combinations(range(n), 2):
    dists[(i, j)] = round(np.linalg.norm(bucu[i] - bucu[j]), 6)
min_d = min(dists.values())
edges = sorted([e for e, d in dists.items() if abs(d - min_d) < 1e-6])

G = nx.Graph()
G.add_nodes_from(range(n))
G.add_edges_from(edges)

V, E = G.number_of_nodes(), G.number_of_edges()
hull = ConvexHull(bucu)

# Kira muka sebenar dengan cantumkan simplex segitiga sepesawat (coplanar)
# supaya segiempat (yang dipecah hull kepada 2 segitiga) dikira sebagai 1 muka.
normals = np.round(hull.equations[:, :3] / np.linalg.norm(hull.equations[:, :3], axis=1, keepdims=True), 4)
offsets = np.round(hull.equations[:, 3], 4)
plane_keys = [tuple(list(nrm) + [off]) for nrm, off in zip(normals, offsets)]
F = len(set(plane_keys))

euler = V - E + F
degrees = dict(G.degree())

print("=== KUBOKTAHEDRON (Ketupat 3 Daun) ===")
print(f"V = {V}, E = {E}, F = {F}  (jangka: 12, 24, 14)")
print(f"V - E + F = {euler}  (mesti = 2)")
print(f"Semua bucu darjah 4? {all(d == 4 for d in degrees.values())}")
assert (V, E, F) == (12, 24, 14)
assert euler == 2
assert all(d == 4 for d in degrees.values())
print("[LULUS] Teorem Euler & ke-4-sekataan graf disahkan.\n")

# ---------- Penguraian kepada 3 daun (versi diperbetulkan) ----------
daun_1 = [0, 4, 3, 8, 10, 9, 1, 6, 0]
daun_2 = [2, 5, 6, 4, 7, 3, 11, 9, 2]
daun_3 = [0, 8, 11, 2, 7, 5, 1, 10, 0]

def path_to_edges(path):
    return [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]

def verify_leaf(name, path, G):
    assert path[0] == path[-1], f"{name}: bukan gelung tertutup"
    interior = path[:-1]
    assert len(set(interior)) == len(interior), f"{name}: bucu berulang -> bukan kitaran ringkas"
    es = path_to_edges(path)
    for e in es:
        assert G.has_edge(*e), f"{name}: sisi {e} bukan sisi kuboktahedron sebenar"
    assert len(set(es)) == len(es), f"{name}: sisi berulang"
    return set(es), set(interior)

leaves = {}
for nm, p in [("Daun 1", daun_1), ("Daun 2", daun_2), ("Daun 3", daun_3)]:
    Ei, Vi = verify_leaf(nm, p, G)
    leaves[nm] = (Ei, Vi)
    print(f"{nm}: {len(Ei)} sisi, melawat {len(Vi)} bucu -> {sorted(Vi)}")

E1, E2, E3 = leaves["Daun 1"][0], leaves["Daun 2"][0], leaves["Daun 3"][0]
full_E = set(tuple(sorted(e)) for e in G.edges())

print(f"\nJumlah |E1|+|E2|+|E3| = {len(E1)+len(E2)+len(E3)} (mesti 24)")
print(f"E1 n E2 = {E1 & E2}")
print(f"E1 n E3 = {E1 & E3}")
print(f"E2 n E3 = {E2 & E3}")
print(f"E1 u E2 u E3 == E (semua sisi)? {(E1|E2|E3) == full_E}")
assert len(E1 & E2) == 0 and len(E1 & E3) == 0 and len(E2 & E3) == 0
assert E1 | E2 | E3 == full_E

# Semak setiap bucu disentuh oleh TEPAT 2 daripada 3 daun (masing2 2 sisi = darjah 4)
print("\nBucu -> daun yang menyentuhnya (mesti tepat 2 daun setiap bucu):")
ok = True
for v in range(n):
    touching = [nm for nm, (Ei, Vi) in leaves.items() if v in Vi]
    print(f"  bucu {v}: {touching}")
    if len(touching) != 2:
        ok = False
assert ok, "GAGAL: ada bucu tidak disentuh oleh tepat 2 daun"
print("\n[LULUS] Setiap satu daripada 12 bucu disentuh oleh tepat 2 daripada 3 daun.")
print("[LULUS] Ketiga-tiga daun ialah kitaran ringkas 8-sisi, sisi-asing, dan menutup kesemua 24 sisi.\n")

print("KESIMPULAN: penguraian 3-daun pada kuboktahedron memenuhi Definisi 2:")
print(" - V=12, E=24, F=14, Euler V-E+F=2")
print(" - Penguraian E = E1 u E2 u E3, sisi-asing sepenuhnya")
print(" - Setiap bucu dilalui oleh tepat 2 daun (syarat (iv) Definisi 2)")
