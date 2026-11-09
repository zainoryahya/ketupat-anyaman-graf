# -*- coding: utf-8 -*-
"""
Pengesahan: Antiprisma heksagon sebagai model 3-daun tanpa lipatan (bahagian 'Anyaman Tanpa Lipatan pada Keluarga Antiprisma' dalam manuskrip)

Dakwaan yang disahkan (setiap satu dilindungi assert; senyap = lulus):
  1. Antiprisma heksagon: V=12, E=24, F=14 (12 segi tiga + 2 heksagon), 4-sekata.
  2. Penguraian laluan terus = tepat 3 kitaran ringkas lapan-sisi, memenuhi
     keempat-empat syarat Definisi 2 -> anyaman 3-daun seimbang dengan SIFAR lipatan.
  3. Carian tuntas ke atas 3^12 sistem peralihan:
       - antiprisma heksagon: penguraian seimbang wujud hanya bagi n = 2 dan n = 3;
         n=3 mempunyai 134 penguraian, tepat 1 daripadanya laluan terus penuh (12 bucu terus).
       - kuboktahedron: n=3 mempunyai 72 penguraian; maksimum 6 bucu terus
         (48 penguraian), 24 penguraian dengan 4 bucu terus.
  4. Dengan susunan atas-bawah berselang-seli, tiga daun laluan terus membentuk
     gambar rajah pautan berselang-seli yang konsisten; graf unjurannya 4-terhubung
     (tiada silangan nugatori), maka menurut Menasco (1984) pautan itu tidak terpisah:
     tiada daun boleh ditarik keluar tanpa merungkai anyaman.
  5. Pelengkap: kuboktahedron mempunyai 3217 penguraian sah (daripada 3^12 sistem);
     n=5 wujud jika tidak seimbang (292 penguraian, cth. panjang 6+5+3+5+5), n=7 mustahil.
     Oktahedron: kesemua 6 penguraian 2-daun mempunyai tepat 2 bucu terus.
Keperluan: numpy, scipy, networkx. Masa larian: ~10-20 saat.
"""
import itertools
import collections
import numpy as np
import networkx as nx
from scipy.spatial import ConvexHull

TOL = 1e-6


# ---------------------------------------------------------------- pembinaan
def antiprisma(m):
    """Antiprisma m-gon dengan sisi tapak = sisi sisian = 1."""
    R = 1.0 / (2 * np.sin(np.pi / m))                      # jejari gelang
    lat2 = 2 * R**2 * (1 - np.cos(np.pi / m))              # jarak mendatar^2 ke jiran gelang lain
    h = np.sqrt(1 - lat2) / 2                              # separuh tinggi
    atas = [(R * np.cos(2*np.pi*k/m), R * np.sin(2*np.pi*k/m), h) for k in range(m)]
    bawah = [(R * np.cos(2*np.pi*(k+.5)/m), R * np.sin(2*np.pi*(k+.5)/m), -h) for k in range(m)]
    return np.array(atas + bawah)


def kuboktahedron():
    pts = set()
    for p in set(itertools.permutations((1, 1, 0))):
        for sg in itertools.product((1, -1), repeat=3):
            pts.add(tuple(s * x for s, x in zip(sg, p)))
    return np.array(sorted(pts), float)


def bina_sisi(P):
    D = np.linalg.norm(P[:, None] - P[None], axis=2)
    dmin = D[D > TOL].min()
    return {frozenset((i, j)) for i in range(len(P)) for j in range(i+1, len(P))
            if abs(D[i, j] - dmin) < TOL}


def kira_muka(P):
    """Bilangan muka hull cembung selepas simplex sepesawat digabungkan."""
    hull = ConvexHull(P)
    satah = []
    for eq in hull.equations:
        if not any(np.allclose(eq, s, atol=1e-6) for s in satah):
            satah.append(eq)
    darjah = []
    for s in satah:
        on = [i for i in range(len(P)) if abs(s[:3] @ P[i] + s[3]) < 1e-6]
        darjah.append(len(on))
    return len(satah), collections.Counter(darjah)


def sistem_putaran(P, E):
    adj = collections.defaultdict(list)
    for e in E:
        i, j = tuple(e)
        adj[i].append(j); adj[j].append(i)
    rot = {}
    for v in range(len(P)):
        n = P[v] / np.linalg.norm(P[v])
        a = P[adj[v][0]] - P[v]; a -= (a @ n) * n; a /= np.linalg.norm(a)
        b = np.cross(n, a)
        rot[v] = sorted(adj[v], key=lambda u: np.arctan2((P[u]-P[v]) @ b, (P[u]-P[v]) @ a))
    return rot


# ---------------------------------------------------------------- penguraian
def jejak(rot, sistem):
    """sistem[v] in {0,1,2}: 0 = terus, 1 dan 2 = membelok. Pulangkan senarai jejak (senarai bucu)."""
    pas = {}
    for v, s in enumerate(sistem):
        a, b, c, d = rot[v]
        pasangan = [((a, c), (b, d)), ((a, b), (c, d)), ((a, d), (b, c))][s]
        for x, y in pasangan:
            pas[(v, x)] = y; pas[(v, y)] = x
    guna, hasil = set(), []
    for v in range(len(rot)):
        for u in rot[v]:
            if frozenset((v, u)) in guna:
                continue
            laluan = [v]; prev, cur = v, u; guna.add(frozenset((v, u)))
            while True:
                laluan.append(cur)
                nxt = pas[(cur, prev)]
                if frozenset((cur, nxt)) in guna:
                    break
                guna.add(frozenset((cur, nxt))); prev, cur = cur, nxt
            hasil.append(laluan[:-1])
    return hasil


def semak_definisi2(E, daun, V):
    """Keempat-empat syarat Definisi 2 menggunakan NetworkX dan operasi set."""
    set_daun = []
    for L in daun:
        Ei = {frozenset((L[k], L[(k+1) % len(L)])) for k in range(len(L))}
        G = nx.Graph([tuple(e) for e in Ei])
        assert all(d == 2 for _, d in G.degree()) and nx.is_connected(G), "(i) gagal"
        set_daun.append(Ei)
    assert set().union(*set_daun) == E, "(ii) gagal"
    for A, B in itertools.combinations(set_daun, 2):
        assert not (A & B), "(iii) gagal"
    for v in range(V):
        assert sum(any(v in e for e in Ei) for Ei in set_daun) == 2, "(iv) gagal"


def carian_tuntas(rot):
    sah = []
    for sistem in itertools.product(range(3), repeat=len(rot)):
        daun = jejak(rot, sistem)
        if all(len(set(L)) == len(L) for L in daun):
            sah.append((sistem, daun))
    return sah


# ---------------------------------------------------------------- pautan
def susunan_berselang_seli(daun):
    """Cari fasa atas/bawah bagi setiap daun supaya di setiap silangan satu atas, satu bawah."""
    for fasa in itertools.product((0, 1), repeat=len(daun)):
        atas = collections.defaultdict(list)
        for i, L in enumerate(daun):
            for k, v in enumerate(L):
                atas[v].append((k + fasa[i]) % 2 == 0)
        if all(sorted(x) == [False, True] for x in atas.values()):
            return fasa
    return None


def nombor_pautan(P, daun, fasa):
    """Nombor pautan berpasangan (tanda silangan dari normal luar sfera)."""
    info = collections.defaultdict(list)
    for i, L in enumerate(daun):
        n = len(L)
        for k, v in enumerate(L):
            t = P[L[(k+1) % n]] - P[L[(k-1) % n]]
            info[v].append((i, t, (k + fasa[i]) % 2 == 0))
    lk = collections.Counter()
    for v, ((i, ti, oi), (j, tj, oj)) in info.items():
        atas_t, bawah_t = (ti, tj) if oi else (tj, ti)
        tanda = np.sign(np.cross(atas_t, bawah_t) @ P[v])
        lk[tuple(sorted((i, j)))] += tanda
    return {k: int(v // 2) for k, v in lk.items()}


# ================================================================ utama
if __name__ == "__main__":
    # ---- 1. data asas antiprisma heksagon
    P = antiprisma(6)
    E = bina_sisi(P)
    V = len(P)
    F, darjah_muka = kira_muka(P)
    assert (V, len(E), F) == (12, 24, 14)
    assert darjah_muka == collections.Counter({3: 12, 6: 2})
    deg = collections.Counter(v for e in E for v in e)
    assert all(deg[v] == 4 for v in range(V))
    assert V - len(E) + F == 2

    # ---- 2. penguraian laluan terus
    rot = sistem_putaran(P, E)
    terus = jejak(rot, (0,) * V)
    assert sorted(len(L) for L in terus) == [8, 8, 8]
    semak_definisi2(E, terus, V)
    # setiap daun: 2 sisi gelang atas, 2 sisi gelang bawah, 4 sisi sisian
    for L in terus:
        sisi = [(L[k], L[(k+1) % 8]) for k in range(8)]
        assert sum(a < 6 and b < 6 for a, b in sisi) == 2
        assert sum(a >= 6 and b >= 6 for a, b in sisi) == 2
    # putaran 60 darjah memetakan setiap daun kepada daun lain (ketiga-tiganya kongruen)
    putar = lambda v: (v + 1) % 6 if v < 6 else 6 + (v - 6 + 1) % 6
    set_daun = [frozenset(frozenset((L[k], L[(k+1) % 8])) for k in range(8)) for L in terus]
    imej = [frozenset(frozenset(map(putar, e)) for e in Ei) for Ei in set_daun]
    assert set(imej) == set(set_daun) and all(imej[i] != set_daun[i] for i in range(3))

    # ---- 3. carian tuntas, antiprisma heksagon lawan kuboktahedron
    sah_ap = carian_tuntas(rot)
    seimbang_ap = collections.defaultdict(list)
    for s, d in sah_ap:
        if len({len(L) for L in d}) == 1:
            seimbang_ap[len(d)].append(s)
    assert set(seimbang_ap) == {2, 3}
    assert len(seimbang_ap[3]) == 134
    assert sum(s.count(0) == 12 for s in seimbang_ap[3]) == 1

    Pk = kuboktahedron()
    Ek = bina_sisi(Pk)
    rotk = sistem_putaran(Pk, Ek)
    sah_k = carian_tuntas(rotk)
    n3_k = [s for s, d in sah_k if len(d) == 3 and {len(L) for L in d} == {8}]
    assert len(n3_k) == 72
    taburan_k = collections.Counter(s.count(0) for s in n3_k)
    assert taburan_k == collections.Counter({6: 48, 4: 24})
    # kuboktahedron: jumlah penguraian sah, dan n=5 wujud jika tidak seimbang
    assert len(sah_k) == 3217
    n5_k = [d for s, d in sah_k if len(d) == 5]
    assert len(n5_k) == 292
    assert any(sorted(len(L) for L in d) == [3, 5, 5, 5, 6] for d in n5_k)
    assert not any(len(d) == 7 for s, d in sah_k)
    # oktahedron: kesemua 6 penguraian 2-daun mempunyai tepat 2 bucu terus (lipatan terpaksa)
    Po = np.array([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)], float)
    roto = sistem_putaran(Po, bina_sisi(Po))
    n2_o = [s for s, d in carian_tuntas(roto) if len(d) == 2]
    assert len(n2_o) == 6 and all(s.count(0) == 2 for s in n2_o)

    # ---- 4. pautan berselang-seli dan tidak terpisah
    fasa = susunan_berselang_seli(terus)
    assert fasa is not None, "tiada susunan atas-bawah berselang-seli yang konsisten"
    G = nx.Graph([tuple(e) for e in E])
    assert nx.node_connectivity(G) == 4          # tiada bucu potong -> tiada silangan nugatori
    lk = nombor_pautan(P, terus, fasa)

    print("Antiprisma heksagon: V, E, F =", V, len(E), F, "| muka:", dict(darjah_muka))
    print("Daun laluan terus:", terus)
    print("Penguraian seimbang (antiprisma):", {n: len(s) for n, s in sorted(seimbang_ap.items())})
    print("n=3 antiprisma, taburan bucu terus:",
          dict(sorted(collections.Counter(s.count(0) for s in seimbang_ap[3]).items())))
    print("n=3 kuboktahedron, taburan bucu terus:", dict(sorted(taburan_k.items())))
    print("Nombor pautan berpasangan (berselang-seli):", lk)
    print("Semua dakwaan lulus.")
