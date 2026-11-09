"""
Pengesahan model Ketupat 2-Daun (Oktahedron).
Mengesahkan dakwaan dalam manuskrip (bahagian 'Model 2-Daun'):
  1. V, E, F dan Teorem Euler V - E + F = 2
  2. Setiap bucu berdarjah genap (darjah 4)
  3. Penguraian graf kepada 2 kitaran sisi-asing (Daun 1, Daun 2) yang
     menutupi kesemua sisi tepat sekali (E = E1 U E2, E1 ^ E2 = kosong)
  4. Setiap laluan daun ialah satu kitaran tunggal (bukan gabungan gelung kecil)
"""
import numpy as np
import networkx as nx
from itertools import combinations
from scipy.spatial import ConvexHull

# ---------- 1. Bina bucu oktahedron ----------
bucu = np.array([
    [ 1, 0, 0],   # 0 Kanan
    [-1, 0, 0],   # 1 Kiri
    [ 0, 1, 0],   # 2 Depan
    [ 0,-1, 0],   # 3 Belakang
    [ 0, 0, 1],   # 4 Atas
    [ 0, 0,-1],   # 5 Bawah
], dtype=float)
n = len(bucu)

# ---------- 2. Bina sisi (edge) secara geometri, bukan hardcode ----------
dists = {}
for i, j in combinations(range(n), 2):
    d = np.linalg.norm(bucu[i] - bucu[j])
    dists[(i, j)] = round(d, 6)
min_d = min(dists.values())
edges = sorted([e for e, d in dists.items() if abs(d - min_d) < 1e-6])

G = nx.Graph()
G.add_nodes_from(range(n))
G.add_edges_from(edges)

V = G.number_of_nodes()
E = G.number_of_edges()

# ---------- 3. F melalui hull cembung sebenar (bukan andaian) ----------
hull = ConvexHull(bucu)
F = len(hull.simplices)

euler = V - E + F
degrees = dict(G.degree())

print("=== OKTAHEDRON (Ketupat 2 Daun) ===")
print(f"V = {V}, E = {E}, F = {F}")
print(f"V - E + F = {euler}  (mesti = 2)")
print(f"Darjah bucu: {degrees}")
assert euler == 2, "GAGAL: Teorem Euler tidak dipenuhi"
assert all(d == 4 for d in degrees.values()), "GAGAL: bukan graf 4-sekata"
print("[LULUS] Teorem Euler V-E+F=2 disahkan; graf 4-sekata disahkan.\n")

# ---------- 4. Penguraian kepada 2 daun (kitaran ringkas tertutup) ----------
daun_1 = [4, 0, 3, 5, 2, 1, 4]
daun_2 = [4, 2, 0, 5, 1, 3, 4]

def path_to_edges(path):
    return [tuple(sorted((path[i], path[i+1]))) for i in range(len(path)-1)]

def verify_leaf(name, path, G):
    assert path[0] == path[-1], f"{name}: laluan tidak kembali ke titik asal"
    interior = path[:-1]
    assert len(set(interior)) == len(interior), f"{name}: bucu berulang (bukan kitaran ringkas)"
    es = path_to_edges(path)
    for e in es:
        assert G.has_edge(*e), f"{name}: sisi {e} tidak wujud dalam graf oktahedron"
    assert len(set(es)) == len(es), f"{name}: ada sisi berulang dalam laluan sendiri"
    return set(es), set(interior)

E1, V1 = verify_leaf("Daun 1", daun_1, G)
E2, V2 = verify_leaf("Daun 2", daun_2, G)

full_E = set(tuple(sorted(e)) for e in G.edges())
print(f"|E1| = {len(E1)}, |E2| = {len(E2)}")
print(f"E1 union E2 == E (semua sisi graf)?  {E1 | E2 == full_E}")
print(f"E1 sisi-asing E2 (tiada pertindihan)? {len(E1 & E2) == 0}")
assert E1 | E2 == full_E
assert len(E1 & E2) == 0
assert V1 == set(range(n)) and V2 == set(range(n)), "Setiap daun mesti melawat semua bucu"
print("[LULUS] Penguraian graf E = E1 u E2, E1 n E2 = {} disahkan.")
print("[LULUS] Daun 1 & Daun 2 setiap satu ialah kitaran Hamilton (6 sisi, 6 bucu).\n")

print("KESIMPULAN: penguraian 2-daun pada oktahedron memenuhi Definisi 2:")
print(" - Kelongsong tertutup (Euler V-E+F=2)")
print(" - Setiap bucu darjah genap = 4 (2 daripada setiap daun)")
print(" - Dua daun ialah kitaran Hamilton sisi-asing yang meliputi kesemua sisi")
