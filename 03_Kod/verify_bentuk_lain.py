"""
Menguji sama ada bentuk ketupat tradisional yang LAIN muat dalam rangka kerja
graf 4-sekata kertas kerja ini.

NOTA: kesimpulan asal skrip ini (bentuk ditolak) telah diperbetulkan; lihat
verify_graf_medial.py.

Motivasi: satu cadangan penambahbaikan mengesyorkan agar Ketupat Palas
dikaitkan dengan TETRAHEDRON dan Ketupat Pasar dengan PRISMA memanjang.
Skrip ini menyemak dakwaan tersebut secara langsung, kerana Andaian 1
kertas kerja menuntut SETIAP bucu berdarjah tepat 4.

Ia juga mencari keluarga polihedron yang benar-benar 4-sekata dan boleh
menampung bentuk ketupat memanjang -- iaitu ANTIPRISMA.
"""
import numpy as np
import networkx as nx
from itertools import combinations


def graf_dari_koordinat(bucu, toleransi=1e-6):
    d = {(i, j): round(float(np.linalg.norm(bucu[i] - bucu[j])), 6)
         for i, j in combinations(range(len(bucu)), 2)}
    dmin = min(d.values())
    sisi = [e for e, v in d.items() if abs(v - dmin) < toleransi]
    G = nx.Graph(); G.add_nodes_from(range(len(bucu))); G.add_edges_from(sisi)
    return G


def lapor(nama, G, F=None):
    V, E = G.number_of_nodes(), G.number_of_edges()
    darjah = sorted({d for _, d in G.degree()})
    empat = (darjah == [4])
    baris = f"{nama:<34} V={V:<3} E={E:<3}"
    if F is not None:
        baris += f" F={F:<3} V-E+F={V-E+F:<3}"
    baris += f" darjah={darjah}"
    baris += "  -> 4-SEKATA ✓" if empat else "  -> BUKAN 4-sekata ✗"
    print(baris)
    if not empat:
        print(f"{'':36}   E=2V? {E} vs {2*V}  -> Andaian 1 GAGAL, "
              f"rangka kerja tidak terpakai")
    return empat


print("=" * 78)
print("A. MENYEMAK CADANGAN: tetrahedron dan prisma")
print("=" * 78)

tetra = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float)
lapor("Tetrahedron (Ketupat Palas?)", graf_dari_koordinat(tetra), F=4)

# prisma segi tiga
h = 1.0
prisma3 = np.array([[np.cos(a), np.sin(a), z]
                    for z in (-h, h)
                    for a in (0, 2*np.pi/3, 4*np.pi/3)], dtype=float)
G_p3 = nx.Graph()
G_p3.add_edges_from([(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])
lapor("Prisma segi tiga (Ketupat Pasar?)", G_p3, F=5)

# prisma segi empat (kubus)
G_p4 = nx.Graph()
G_p4.add_edges_from([(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                     (0,4),(1,5),(2,6),(3,7)])
lapor("Prisma segi empat (kubus)", G_p4, F=6)

print("\n" + "=" * 78)
print("B. ALTERNATIF YANG SAH: keluarga ANTIPRISMA (semuanya 4-sekata)")
print("=" * 78)


def antiprisma(n, tinggi=1.0):
    """Antiprisma n-gon: dua gelang n-gon diputar 180/n darjah."""
    bucu = []
    for k in range(n):
        a = 2 * np.pi * k / n
        bucu.append([np.cos(a), np.sin(a), tinggi / 2])
    for k in range(n):
        a = 2 * np.pi * (k + 0.5) / n
        bucu.append([np.cos(a), np.sin(a), -tinggi / 2])
    return np.array(bucu)


def graf_antiprisma(n):
    G = nx.Graph()
    for k in range(n):
        G.add_edge(k, (k + 1) % n)                    # gelang atas
        G.add_edge(n + k, n + (k + 1) % n)            # gelang bawah
        G.add_edge(k, n + k)                          # sisi serong
        G.add_edge(k, n + (k - 1) % n)
    return G


def penguraian_seimbang(G, n_daun):
    """Cari penguraian sisi-asing kepada n_daun kitaran ringkas sama panjang."""
    E = {tuple(sorted(e)) for e in G.edges()}
    L = len(E) // n_daun
    if len(E) % n_daun or not (3 <= L <= G.number_of_nodes()):
        return None
    kit = set()
    def dfs(mula, kini, laluan, dilawat):
        if len(laluan) == L:
            if G.has_edge(kini, mula):
                f = frozenset(tuple(sorted((laluan[i], laluan[(i+1) % L])))
                              for i in range(L))
                if len(f) == L:
                    kit.add(f)
            return
        for w in G.neighbors(kini):
            if w >= mula and w not in dilawat:
                dfs(mula, w, laluan + [w], dilawat | {w})
    for s in G.nodes():
        dfs(s, s, [s], {s})
    kit = sorted(kit, key=lambda f: sorted(f))
    ikut = {e: [c for c in kit if e in c] for e in E}
    def cari(belum, pilih):
        if not belum:
            return pilih if len(pilih) == n_daun else None
        if len(pilih) == n_daun:
            return None
        for c in ikut[min(belum)]:
            if c <= belum:
                r = cari(belum - c, pilih + [c])
                if r:
                    return r
        return None
    return cari(frozenset(E), [])


for n in (3, 4, 5, 6):
    G = graf_antiprisma(n)
    V, E = G.number_of_nodes(), G.number_of_edges()
    F = 2 - V + E
    ok = lapor(f"Antiprisma {n}-gon", G, F=F)
    if not ok:
        continue
    boleh = []
    for nd in range(2, E // 3 + 1):
        if E % nd:
            continue
        if penguraian_seimbang(G, nd):
            boleh.append(nd)
    print(f"{'':36}   anyaman seimbang wujud bagi n = {boleh}")

print("\n" + "=" * 78)
print("KESIMPULAN")
print("=" * 78)
print("Tetrahedron dan prisma ialah graf 3-SEKATA, jadi BUCUNYA tidak boleh menjadi")
print("titik pertemuan dua jalur (Andaian 1). Namun ini tidak menolak BENTUK itu:")
print("penjuru bentuk bukan bucu graf. Graf persilangan bagi kelongsong berbentuk P")
print("ialah graf medial M(P), yang sentiasa 4-sekata -- M(tetrahedron) = oktahedron.")
print("Lihat verify_graf_medial.py dan bahagian 'Skop dan Had Rangka Kerja' dalam manuskrip.")
print()
print("Antiprisma pula 4-sekata bagi semua n (M(piramid n-gon) = antiprisma n-gon),")
print("dan boleh dipanjangkan di sepanjang paksi tanpa mengubah graf -- calon")
print("semula jadi bagi ketupat memanjang.")
