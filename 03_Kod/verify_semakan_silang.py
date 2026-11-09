# -*- coding: utf-8 -*-
"""
Pengesahan: semakan silang bilangan penguraian, Jadual 4, Proposisi antiprisma
dan sifat Brunnian (bahagian 'Protokol Pengesahan Berkomputer',
'Analisis Laluan Terus' dan 'Anyaman Tanpa Lipatan pada Keluarga Antiprisma' dalam manuskrip).

Dakwaan (setiap satu dilindungi assert; senyap = lulus):
  1. Bilangan penguraian sah (semua jejak kitaran ringkas) dikira melalui DUA kaedah bebas:
     (a) penjejakan kesemua 3^V sistem peralihan, (b) exact cover ke atas semua kitaran
     ringkas graf. Kedua-duanya memberi 43 (oktahedron), 3217 (kuboktahedron),
     2169 (antiprisma heksagon).
  2. Jadual 4: bucu terus maksimum (dan bilangan penguraian) bagi n = 2, 3, 4.
  3. Proposisi (laluan terus pada antiprisma m-gon): tiga kitaran ringkas sepanjang 4m/3
     jika 3 | m; satu jejak sepanjang 4m yang melalui setiap bucu dua kali jika 3 tidak
     membahagi m. Disemak bagi 3 <= m <= 15, termasuk susunan siklik jiran yang
     digunakan dalam bukti.
  4. Sifat Brunnian bagi m = 3, 6, 9, 12: dengan susunan atas-bawah berselang-seli,
     bagi setiap pasangan daun satu daun sentiasa di atas daun yang lain (corak kitaran),
     jadi setiap pasangan boleh dipisahkan; tiada daun bersilang dengan dirinya; gambar
     rajah terhubung (Menasco 1984 -> pautan penuh tidak terpisah).
Keperluan: numpy, scipy, networkx. Masa larian: ~30 saat.
"""
import collections
import itertools
import numpy as np
import networkx as nx

from verify_antiprisma_heksagon import (antiprisma, kuboktahedron, bina_sisi,
                                        sistem_putaran, jejak, carian_tuntas,
                                        susunan_berselang_seli)


def oktahedron():
    return np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)


# ------------------------------------------------------------ exact cover
def semua_kitaran_ringkas(E):
    G = nx.Graph([tuple(e) for e in E])
    hasil = set()

    def dfs(mula, kini, laluan, lawat):
        for w in G.neighbors(kini):
            if w == mula and len(laluan) >= 3:
                hasil.add(frozenset(frozenset((laluan[i], laluan[(i + 1) % len(laluan)]))
                                    for i in range(len(laluan))))
            elif w > mula and w not in lawat:
                dfs(mula, w, laluan + [w], lawat | {w})

    for s in G.nodes():
        dfs(s, s, [s], {s})
    return list(hasil)


def kira_exact_cover(E, kitaran):
    ikut = collections.defaultdict(list)
    for c in kitaran:
        for e in c:
            ikut[e].append(c)
    kiraan = [0]

    def cari(belum):
        if not belum:
            kiraan[0] += 1
            return
        e = min(belum, key=lambda x: sorted(x))
        for c in ikut[e]:
            if c <= belum:
                cari(belum - c)

    cari(frozenset(E))
    return kiraan[0]


# ------------------------------------------------------------ utama
if __name__ == "__main__":
    graf = {"Oktahedron": oktahedron(), "Kuboktahedron": kuboktahedron(),
            "Antiprisma heksagon": antiprisma(6)}
    jangka_jumlah = {"Oktahedron": 43, "Kuboktahedron": 3217, "Antiprisma heksagon": 2169}
    # Jadual 4: n -> (bucu terus maksimum, bilangan penguraian seimbang)
    jangka_jadual = {
        "Oktahedron": {2: (2, 6), 3: (6, 7), 4: (0, 2)},
        "Kuboktahedron": {2: (8, 48), 3: (6, 72), 4: (12, 61), 6: (0, 1), 8: (0, 1)},
        "Antiprisma heksagon": {2: (2, 12), 3: (12, 134)},
    }

    # ---- 1 & 2
    for nama, P in graf.items():
        E = bina_sisi(P)
        rot = sistem_putaran(P, E)
        sah = carian_tuntas(rot)
        kit = semua_kitaran_ringkas(E)
        ec = kira_exact_cover(E, kit)
        assert len(sah) == ec == jangka_jumlah[nama], (nama, len(sah), ec)
        seimb = collections.defaultdict(list)
        for s, d in sah:
            if len({len(L) for L in d}) == 1:
                seimb[len(d)].append(s)
        jadual = {n: (max(s.count(0) for s in v), len(v)) for n, v in sorted(seimb.items())}
        assert jadual == jangka_jadual[nama], (nama, jadual)
        print(f"{nama}: sistem peralihan = exact cover = {ec}; Jadual 4: {jadual}")

    # ---- 3: Proposisi antiprisma
    for m in range(3, 16):
        P = antiprisma(m)
        E = bina_sisi(P)
        rot = sistem_putaran(P, E)
        a = lambda k: k % m
        b = lambda k: m + k % m

        def sama_siklik(r, sasaran):
            for t in range(4):
                rr = r[t:] + r[:t]
                if rr == sasaran or rr == sasaran[::-1]:
                    return True
            return False

        for k in range(m):
            assert sama_siklik(rot[a(k)], [a(k + 1), b(k), b(k - 1), a(k - 1)])
            assert sama_siklik(rot[b(k)], [b(k + 1), a(k + 1), a(k), b(k - 1)])
        terus = jejak(rot, (0,) * (2 * m))
        if m % 3 == 0:
            assert sorted(len(L) for L in terus) == [4 * m // 3] * 3
            assert all(len(set(L)) == len(L) for L in terus)
        else:
            assert len(terus) == 1 and len(terus[0]) == 4 * m
            assert all(c == 2 for c in collections.Counter(terus[0]).values())
    print("Proposisi antiprisma: lulus bagi 3 <= m <= 15")

    # ---- 4: Brunnian (dominasi kitaran) bagi m = 3, 6, 9, 12
    for m in (3, 6, 9, 12):
        P = antiprisma(m)
        E = bina_sisi(P)
        rot = sistem_putaran(P, E)
        daun = jejak(rot, (0,) * (2 * m))
        fasa = susunan_berselang_seli(daun)
        assert fasa is not None
        atas = collections.defaultdict(list)          # bucu -> [(daun, di_atas?)]
        for i, L in enumerate(daun):
            for k, v in enumerate(L):
                atas[v].append((i, (k + fasa[i]) % 2 == 0))
        dominasi = collections.defaultdict(set)       # (i, j) -> set daun yang di atas
        for v, lst in atas.items():
            (i, oi), (j, oj) = lst
            assert i != j                             # tiada silangan sendiri
            assert oi != oj
            dominasi[tuple(sorted((i, j)))].add(i if oi else j)
        assert len(dominasi) == 3 and all(len(x) == 1 for x in dominasi.values())
        # corak kitaran: setiap daun di atas tepat satu daun lain
        pemenang = collections.Counter(next(iter(x)) for x in dominasi.values())
        assert sorted(pemenang.values()) == [1, 1, 1]
        G = nx.Graph([tuple(e) for e in E])
        assert nx.is_connected(G)
    print("Brunnian (dominasi kitaran): lulus bagi m = 3, 6, 9, 12")
    print("Semua dakwaan lulus.")
